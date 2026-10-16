"""Builds the AS-IS and TO-BE BPMN 2.0 files (semantic model + diagram layout).

Run: python bpmn_build.py  -> writes as_is.bpmn and to_be.bpmn next to this script.
The .bpmn files open in Camunda Modeler or https://demo.bpmn.io.
"""
from pathlib import Path
from xml.sax.saxutils import escape

SIZES = {
    "startEvent": (36, 36), "endEvent": (36, 36), "intermediateCatchEvent": (36, 36),
    "exclusiveGateway": (50, 50), "parallelGateway": (50, 50),
    "task": (100, 80), "userTask": (100, 80), "serviceTask": (100, 80),
    "sendTask": (100, 80), "businessRuleTask": (100, 80), "manualTask": (100, 80),
    "dataStoreReference": (50, 50),
}


PALETTE = {
    "task": ("#E3EEFA", "#3B6EA8"), "userTask": ("#E3EEFA", "#3B6EA8"), "sendTask": ("#E3EEFA", "#3B6EA8"),
    "manualTask": ("#E3EEFA", "#3B6EA8"),
    "serviceTask": ("#E2F3F1", "#2A7F8E"),
    "businessRuleTask": ("#FFF4E0", "#C98A1B"),
    "exclusiveGateway": ("#FFF4E0", "#C98A1B"), "parallelGateway": ("#FFF4E0", "#C98A1B"),
    "startEvent": ("#FFFFFF", "#2A7F8E"), "endEvent": ("#FFFFFF", "#B5452F"),
    "intermediateCatchEvent": ("#FFFFFF", "#C98A1B"),
    "dataStoreReference": ("#EEF1F5", "#4A5A70"),
}
PAIN = ("#FBE9E7", "#B5452F")
EDGE = "#4A5A70"


def col(fill, stroke):
    return (f' bioc:fill="{fill}" bioc:stroke="{stroke}"'
            f' color:background-color="{fill}" color:border-color="{stroke}"')


class Diagram:
    def __init__(self, pid, pool_name, pool, lanes):
        self.pid = pid
        self.pool_name = pool_name
        self.pool = pool          # x, y, w, h
        self.lanes = lanes        # list of (id, name, y, h)
        self.nodes = {}           # id -> dict
        self.flows = []
        self.ext_pools = []       # (id, name, x, y, w, h)
        self.messages = []        # (id, name, src, tgt, waypoints, label_xy)
        self.data_in = []         # (store, task, waypoints)
        self.data_out = []        # (task, store, waypoints)
        self.lane_fill = {}       # lane id -> fill
        self.pain = set()         # node ids highlighted as pain points
        self.notes = []           # (id, text, x, y, w, h)

    def node(self, nid, kind, name, cx, cy, lane, label_xy=None, timer=False, message=False):
        w, h = SIZES[kind]
        self.nodes[nid] = dict(kind=kind, name=name, x=cx - w / 2, y=cy - h / 2, w=w, h=h,
                               lane=lane, label=label_xy, timer=timer, message=message)

    def flow(self, fid, src, tgt, pts, name=None, label_xy=None):
        self.flows.append((fid, src, tgt, pts, name, label_xy))

    # ------------------------------------------------------------------ XML
    def xml(self):
        o = []
        a = o.append
        a('<?xml version="1.0" encoding="UTF-8"?>')
        a('<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" '
          'xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" '
          'xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" '
          'xmlns:di="http://www.omg.org/spec/DD/20100524/DI" '
          'xmlns:bioc="http://bpmn.io/schema/bpmn/biocolor/1.0" '
          'xmlns:color="http://www.omg.org/spec/BPMN/non-normative/color/1.0" '
          f'id="Definitions_{self.pid}" targetNamespace="http://example.com/bpmn/hcp-case">')
        a(f'  <bpmn:collaboration id="Collab_{self.pid}">')
        a(f'    <bpmn:participant id="Pool_{self.pid}" name="{escape(self.pool_name)}" processRef="{self.pid}" />')
        for pid, name, *_ in self.ext_pools:
            a(f'    <bpmn:participant id="{pid}" name="{escape(name)}" />')
        for mid, name, src, tgt, *_ in self.messages:
            nm = f' name="{escape(name)}"' if name else ''
            a(f'    <bpmn:messageFlow id="{mid}"{nm} sourceRef="{src}" targetRef="{tgt}" />')
        a('  </bpmn:collaboration>')

        a(f'  <bpmn:process id="{self.pid}" isExecutable="false">')
        a(f'    <bpmn:laneSet id="LaneSet_{self.pid}">')
        for lid, lname, *_ in self.lanes:
            a(f'      <bpmn:lane id="{lid}" name="{escape(lname)}">')
            for nid, n in self.nodes.items():
                if n["lane"] == lid and n["kind"] != "dataStoreReference":
                    a(f'        <bpmn:flowNodeRef>{nid}</bpmn:flowNodeRef>')
            a('      </bpmn:lane>')
        a('    </bpmn:laneSet>')

        for nid, n in self.nodes.items():
            kind, name = n["kind"], escape(n["name"]) if n["name"] else ""
            nm = f' name="{name}"' if name else ""
            if kind == "dataStoreReference":
                a(f'    <bpmn:dataStoreReference id="{nid}"{nm} />')
                continue
            inner = []
            for fid, s, t, *_ in self.flows:
                if t == nid:
                    inner.append(f'      <bpmn:incoming>{fid}</bpmn:incoming>')
            for fid, s, t, *_ in self.flows:
                if s == nid:
                    inner.append(f'      <bpmn:outgoing>{fid}</bpmn:outgoing>')
            ins = [d for d in self.data_in if d[1] == nid]
            outs = [d for d in self.data_out if d[0] == nid]
            if ins:
                inner.append(f'      <bpmn:property id="Prop_{nid}" name="__targetRef_placeholder" />')
                for i, (store, task, _) in enumerate(ins):
                    inner.append(f'      <bpmn:dataInputAssociation id="DIA_{nid}_{i}">'
                                 f'<bpmn:sourceRef>{store}</bpmn:sourceRef>'
                                 f'<bpmn:targetRef>Prop_{nid}</bpmn:targetRef></bpmn:dataInputAssociation>')
            for i, (task, store, _) in enumerate(outs):
                inner.append(f'      <bpmn:dataOutputAssociation id="DOA_{nid}_{i}">'
                             f'<bpmn:targetRef>{store}</bpmn:targetRef></bpmn:dataOutputAssociation>')
            if n["timer"]:
                inner.append(f'      <bpmn:timerEventDefinition id="Timer_{nid}" />')
            if n["message"]:
                inner.append(f'      <bpmn:messageEventDefinition id="Msg_{nid}" />')
            a(f'    <bpmn:{kind} id="{nid}"{nm}>')
            o.extend(inner)
            a(f'    </bpmn:{kind}>')
        for fid, s, t, pts, name, _ in self.flows:
            nm = f' name="{escape(name)}"' if name else ""
            a(f'    <bpmn:sequenceFlow id="{fid}"{nm} sourceRef="{s}" targetRef="{t}" />')
        for nid, text, *_ in self.notes:
            a(f'    <bpmn:textAnnotation id="{nid}"><bpmn:text>{escape(text)}</bpmn:text></bpmn:textAnnotation>')
        a('  </bpmn:process>')

        # ---------------------------------------------------------- DI
        a(f'  <bpmndi:BPMNDiagram id="Diagram_{self.pid}">')
        a(f'    <bpmndi:BPMNPlane id="Plane_{self.pid}" bpmnElement="Collab_{self.pid}">')
        x, y, w, h = self.pool
        a(f'      <bpmndi:BPMNShape id="Pool_{self.pid}_di" bpmnElement="Pool_{self.pid}" isHorizontal="true">'
          f'<dc:Bounds x="{x}" y="{y}" width="{w}" height="{h}" /></bpmndi:BPMNShape>')
        for lid, lname, ly, lh in self.lanes:
            a(f'      <bpmndi:BPMNShape id="{lid}_di" bpmnElement="{lid}" isHorizontal="true">'
              f'<dc:Bounds x="{x + 30}" y="{ly}" width="{w - 30}" height="{lh}" /></bpmndi:BPMNShape>')
        for pid, name, px, py, pw, ph in self.ext_pools:
            a(f'      <bpmndi:BPMNShape id="{pid}_di" bpmnElement="{pid}" isHorizontal="true">'
              f'<dc:Bounds x="{px}" y="{py}" width="{pw}" height="{ph}" /></bpmndi:BPMNShape>')
        for nid, n in self.nodes.items():
            extra = ' isMarkerVisible="true"' if n["kind"] == "exclusiveGateway" else ""
            fill, stroke = PAIN if nid in self.pain else PALETTE[n["kind"]]
            extra += col(fill, stroke)
            a(f'      <bpmndi:BPMNShape id="{nid}_di" bpmnElement="{nid}"{extra}>'
              f'<dc:Bounds x="{n["x"]:.0f}" y="{n["y"]:.0f}" width="{n["w"]}" height="{n["h"]}" />')
            if n["label"]:
                lx, ly, lw, lh = n["label"]
                a(f'        <bpmndi:BPMNLabel><dc:Bounds x="{lx}" y="{ly}" width="{lw}" height="{lh}" /></bpmndi:BPMNLabel>')
            a('      </bpmndi:BPMNShape>')
        for fid, s, t, pts, name, lab in self.flows:
            a(f'      <bpmndi:BPMNEdge id="{fid}_di" bpmnElement="{fid}" bioc:stroke="{EDGE}" color:border-color="{EDGE}">')
            for px, py in pts:
                a(f'        <di:waypoint x="{px}" y="{py}" />')
            if lab:
                lx, ly = lab
                a(f'        <bpmndi:BPMNLabel><dc:Bounds x="{lx}" y="{ly}" width="90" height="27" /></bpmndi:BPMNLabel>')
            a('      </bpmndi:BPMNEdge>')
        for mid, name, s, t, pts, lab in self.messages:
            a(f'      <bpmndi:BPMNEdge id="{mid}_di" bpmnElement="{mid}">')
            for px, py in pts:
                a(f'        <di:waypoint x="{px}" y="{py}" />')
            if lab:
                lx, ly = lab
                a(f'        <bpmndi:BPMNLabel><dc:Bounds x="{lx}" y="{ly}" width="90" height="14" /></bpmndi:BPMNLabel>')
            a('      </bpmndi:BPMNEdge>')
        for kind, lst in (("DIA", self.data_in), ("DOA", self.data_out)):
            for d in lst:
                nid = d[1] if kind == "DIA" else d[0]
                idx = [e for e in lst if (e[1] if kind == "DIA" else e[0]) == nid].index(d)
                a(f'      <bpmndi:BPMNEdge id="{kind}_{nid}_{idx}_di" bpmnElement="{kind}_{nid}_{idx}">')
                for px, py in d[2]:
                    a(f'        <di:waypoint x="{px}" y="{py}" />')
                a('      </bpmndi:BPMNEdge>')
        for nid, text, nx, ny, nw, nh in self.notes:
            a(f'      <bpmndi:BPMNShape id="{nid}_di" bpmnElement="{nid}"><dc:Bounds x="{nx}" y="{ny}" width="{nw}" height="{nh}" /></bpmndi:BPMNShape>')
        a('    </bpmndi:BPMNPlane>')
        a('  </bpmndi:BPMNDiagram>')
        a('</bpmn:definitions>')
        return "\n".join(o)


def lbl_above(cx, cy, w=120):
    return (cx - w / 2, cy - 25 - 34, w, 27)


def lbl_below(cx, cy, w=100):
    return (cx - w / 2, cy + 25 + 5, w, 27)


# ====================================================================== AS-IS
def as_is():
    d = Diagram("Process_AsIs", "PharmaCo after the acquisition (AS-IS)", (160, 80, 1620, 440),
                [("Lane_Rep", "Field reps (PharmaCo and BioCo)", 80, 200),
                 ("Lane_Tr", "Transparency team", 280, 240)])
    R, T = 145, 380
    d.node("S_Met", "startEvent", "Doctor met", 258, R, "Lane_Rep", (228, R + 22, 60, 14))
    d.node("T_SearchOwn", "task", "Search own CRM", 370, R, "Lane_Rep")
    d.node("G_Found", "exclusiveGateway", "Doctor found in own CRM?", 480, R, "Lane_Rep", lbl_above(480, R))
    d.node("T_CreateRec", "task", "Create new doctor record", 590, 235, "Lane_Rep")
    d.node("G_Join1", "exclusiveGateway", None, 760, R, "Lane_Rep")
    d.node("T_Log", "task", "Log visit or payment", 900, R, "Lane_Rep")
    d.node("E_Logged", "endEvent", "Visit logged", 1030, R, "Lane_Rep", (1000, R + 22, 60, 14))
    d.node("DS_Src", "dataStoreReference", "CRMs, events and spend systems", 370, 238, "Lane_Rep",
           (225, 218, 110, 40))

    d.node("S_Cycle", "startEvent", "Annual reporting cycle", 258, T, "Lane_Tr", (213, T + 22, 90, 27), timer=True)
    d.node("T_Export", "task", "Export payments from 3 systems", 370, T, "Lane_Tr")
    d.node("T_Match", "task", "Match doctors by surname and city", 530, T, "Lane_Tr")
    d.node("G_Certain", "exclusiveGateway", "Match certain?", 665, T, "Lane_Tr", lbl_above(665, T, 90))
    d.node("T_Review", "task", "Review ~3,000 pairs by hand (no decision log)", 780, 470, "Lane_Tr")
    d.node("G_Join2", "exclusiveGateway", None, 880, T, "Lane_Tr")
    d.node("T_Totals", "task", "Build totals per doctor", 1000, T, "Lane_Tr")
    d.node("T_IntRev", "task", "Internal review and corrections (~2 weeks)", 1160, T, "Lane_Tr")
    d.node("T_Upload", "sendTask", "Upload report to regulator portals", 1320, T, "Lane_Tr")
    d.node("IE_Dispute", "intermediateCatchEvent", "Dispute received", 1448, T, "Lane_Tr",
           (1408, T - 50, 80, 27), message=True)
    d.node("T_Correct", "task", "Correct totals in spreadsheet", 1570, T, "Lane_Tr")
    d.node("E_Done", "endEvent", "Cycle closed", 1700, T, "Lane_Tr", (1670, T + 22, 60, 14))

    d.flow("F1", "S_Met", "T_SearchOwn", [(276, R), (320, R)])
    d.flow("F2", "T_SearchOwn", "G_Found", [(420, R), (455, R)])
    d.flow("F3", "G_Found", "G_Join1", [(505, R), (735, R)], "Yes", (600, R - 18))
    d.flow("F4", "G_Found", "T_CreateRec", [(480, R + 25), (480, 235), (540, 235)], "No", (486, 190))
    d.flow("F5", "T_CreateRec", "G_Join1", [(640, 235), (760, 235), (760, R + 25)])
    d.flow("F6", "G_Join1", "T_Log", [(785, R), (850, R)])
    d.flow("F7", "T_Log", "E_Logged", [(950, R), (1012, R)])

    d.flow("F10", "S_Cycle", "T_Export", [(276, T), (320, T)])
    d.flow("F11", "T_Export", "T_Match", [(420, T), (480, T)])
    d.flow("F12", "T_Match", "G_Certain", [(580, T), (640, T)])
    d.flow("F13", "G_Certain", "G_Join2", [(690, T), (855, T)], "Yes", (750, T - 18))
    d.flow("F14", "G_Certain", "T_Review", [(665, T + 25), (665, 470), (730, 470)], "No", (671, 425))
    d.flow("F15", "T_Review", "G_Join2", [(830, 470), (880, 470), (880, T + 25)])
    d.flow("F16", "G_Join2", "T_Totals", [(905, T), (950, T)])
    d.flow("F17", "T_Totals", "T_IntRev", [(1050, T), (1110, T)])
    d.flow("F18", "T_IntRev", "T_Upload", [(1210, T), (1270, T)])
    d.flow("F19", "T_Upload", "IE_Dispute", [(1370, T), (1430, T)])
    d.flow("F20", "IE_Dispute", "T_Correct", [(1466, T), (1520, T)])
    d.flow("F21", "T_Correct", "E_Done", [(1620, T), (1682, T)])

    d.data_in.append(("DS_Src", "T_Export", [(370, 263), (370, 340)]))
    d.lane_fill = {"Lane_Rep": "#F5F8FC", "Lane_Tr": "#F7F5FB"}
    d.pain = {"T_CreateRec", "T_Match", "T_Review", "T_IntRev", "T_Correct"}
    d.notes.append(("Note_Legend", "Red: pain points found in discovery (P1 to P5)", 1500, 450, 260, 40))

    d.ext_pools += [("Pool_Regulator", "Regulators (CMS Open Payments, national platforms)", 960, 580, 400, 60),
                    ("Pool_Doctor", "Doctors", 1430, 580, 350, 60)]
    d.messages += [
        ("M1", "Disclosure report", "T_Upload", "Pool_Regulator", [(1320, 420), (1320, 580)], (1326, 540)),
        ("M2", "Published amounts", "Pool_Regulator", "Pool_Doctor", [(1360, 610), (1430, 610)], (1350, 625)),
        ("M3", "Dispute", "Pool_Doctor", "IE_Dispute", [(1448, 580), (1448, 398)], (1454, 540)),
    ]
    return d


# ====================================================================== TO-BE
def to_be():
    d = Diagram("Process_ToBe", "PharmaCo with HCP master data (TO-BE)", (160, 80, 1660, 790),
                [("Lane_Rep", "Field reps", 80, 230),
                 ("Lane_Mdm", "MDM hub (system)", 310, 220),
                 ("Lane_Stw", "Data stewards", 530, 170),
                 ("Lane_Tr", "Transparency team", 700, 170)])
    R, M, S, T = 145, 420, 615, 785
    d.node("S_Met", "startEvent", "Doctor met", 258, R, "Lane_Rep", (228, R + 22, 60, 14))
    d.node("T_Search", "userTask", "Search before create", 370, R, "Lane_Rep")
    d.node("G_Found", "exclusiveGateway", "Right doctor in candidates?", 480, R, "Lane_Rep", lbl_above(480, R, 130))
    d.node("T_Link", "userTask", "Link to golden record", 620, R, "Lane_Rep")
    d.node("T_Create", "userTask", "Create new doctor (US: NPI required)", 590, 255, "Lane_Rep")
    d.node("P_Split", "parallelGateway", None, 700, 255, "Lane_Rep")
    d.node("G_Join", "exclusiveGateway", None, 760, R, "Lane_Rep")
    d.node("T_Log", "userTask", "Log visit or payment", 900, R, "Lane_Rep")
    d.node("E_Logged", "endEvent", "Visit logged", 1030, R, "Lane_Rep", (1000, R + 22, 60, 14))

    d.node("T_Match", "serviceTask", "Apply rules R1 to R8 and score", 700, M, "Lane_Mdm")
    d.node("G_Outcome", "exclusiveGateway", "Outcome?", 830, M, "Lane_Mdm", (765, M + 28, 60, 14))
    d.node("T_Merge", "serviceTask", "Update golden record, log merge event", 1010, M, "Lane_Mdm")
    d.node("G_Join2", "exclusiveGateway", None, 1170, M, "Lane_Mdm")
    d.node("T_Publish", "serviceTask", "Publish golden record to CRMs and reporting", 1310, M, "Lane_Mdm")
    d.node("E_Pub", "endEvent", "Golden record current", 1450, M, "Lane_Mdm", (1410, M + 22, 80, 27))
    d.node("DS_Golden", "dataStoreReference", "Golden records", 1310, 585, "Lane_Stw", (1340, 600, 80, 14))

    d.node("T_Review", "userTask", "Review pair with explanation", 830, S, "Lane_Stw")
    d.node("G_Same", "exclusiveGateway", "Same doctor?", 1010, S, "Lane_Stw", lbl_below(1010, S, 80))

    d.node("S_Cycle", "startEvent", "Reporting cycle", 918, T, "Lane_Tr", (883, T + 22, 70, 14), timer=True)
    d.node("T_Extract", "serviceTask", "Produce extract from golden records", 1030, T, "Lane_Tr")
    d.node("T_Check", "userTask", "Check flagged changes since last extract", 1180, T, "Lane_Tr")
    d.node("T_Basis", "businessRuleTask", "Apply publication basis per country", 1330, T, "Lane_Tr")
    d.node("T_Upload", "sendTask", "Upload report to regulator portals", 1480, T, "Lane_Tr")
    d.node("E_Sub", "endEvent", "Report submitted", 1610, T, "Lane_Tr", (1575, T + 22, 70, 27))

    d.flow("F1", "S_Met", "T_Search", [(276, R), (320, R)])
    d.flow("F2", "T_Search", "G_Found", [(420, R), (455, R)])
    d.flow("F3", "G_Found", "T_Link", [(505, R), (570, R)], "Yes", (520, R - 18))
    d.flow("F4", "G_Found", "T_Create", [(480, R + 25), (480, 255), (540, 255)], "No", (486, 200))
    d.flow("F5", "T_Link", "G_Join", [(670, R), (735, R)])
    d.flow("F6", "T_Create", "P_Split", [(640, 255), (675, 255)])
    d.flow("F7", "P_Split", "G_Join", [(725, 255), (760, 255), (760, R + 25)])
    d.flow("F8", "P_Split", "T_Match", [(700, 280), (700, 380)])
    d.flow("F9", "G_Join", "T_Log", [(785, R), (850, R)])
    d.flow("F10", "T_Log", "E_Logged", [(950, R), (1012, R)])

    d.flow("F20", "T_Match", "G_Outcome", [(750, M), (805, M)])
    d.flow("F21", "G_Outcome", "T_Merge", [(855, M), (960, M)], "Merge by rule or auto-merge", (862, M - 40))
    d.flow("F22", "G_Outcome", "G_Join2", [(830, M - 25), (830, 340), (1170, 340), (1170, M - 25)],
           "Not a duplicate", (1040, 322))
    d.flow("F23", "G_Outcome", "T_Review", [(830, M + 25), (830, 575)], "Review", (836, 490))
    d.flow("F24", "T_Merge", "G_Join2", [(1060, M), (1145, M)])
    d.flow("F25", "G_Join2", "T_Publish", [(1195, M), (1260, M)])
    d.flow("F26", "T_Publish", "E_Pub", [(1360, M), (1432, M)])

    d.flow("F30", "T_Review", "G_Same", [(880, S), (985, S)])
    d.flow("F31", "G_Same", "T_Merge", [(1010, S - 25), (1010, 460)], "Yes", (1016, 520))
    d.flow("F32", "G_Same", "G_Join2", [(1035, S), (1170, S), (1170, M + 25)], "No", (1100, S - 18))

    d.flow("F40", "S_Cycle", "T_Extract", [(936, T), (980, T)])
    d.flow("F41", "T_Extract", "T_Check", [(1080, T), (1130, T)])
    d.flow("F42", "T_Check", "T_Basis", [(1230, T), (1280, T)])
    d.flow("F43", "T_Basis", "T_Upload", [(1380, T), (1430, T)])
    d.flow("F44", "T_Upload", "E_Sub", [(1530, T), (1592, T)])

    d.data_out.append(("T_Publish", "DS_Golden", [(1310, 460), (1310, 560)]))
    d.lane_fill = {"Lane_Rep": "#F5F8FC", "Lane_Mdm": "#F2FAF8", "Lane_Stw": "#FBF8F1", "Lane_Tr": "#F7F5FB"}
    d.notes.append(("Note_Legend", "Blue: people. Teal: system. Amber: decisions and business rules.", 1500, 230, 290, 45))
    d.data_in.append(("DS_Golden", "T_Extract", [(1295, 610), (1050, 745)]))

    d.ext_pools.append(("Pool_Regulator", "Regulators (CMS Open Payments, national platforms)", 1300, 910, 520, 60))
    d.messages.append(("M1", "Disclosure report", "T_Upload", "Pool_Regulator", [(1480, 825), (1480, 910)], (1486, 870)))
    return d


if __name__ == "__main__":
    here = Path(__file__).parent
    (here / "as_is.bpmn").write_text(as_is().xml(), encoding="utf-8")
    (here / "to_be.bpmn").write_text(to_be().xml(), encoding="utf-8")
    print("written")
