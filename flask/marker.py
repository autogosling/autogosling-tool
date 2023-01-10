import copy

MARK_1D = ["rect", "triangleLeft", "triangleRight",
           "rule", "betweenLink", "withinLink", "text"]
MARK_2D = ["rect", "bar", "point", "line", "area", "text"]

DEFAULT_SUBTRACK_2D_BAR = {
    "mark": "bar"
}
DEFAULT_SUBTRACK_2D_AREA = {
    "mark": "area"
}
DEFAULT_SUBTRACK_2D_LINE = {
    "mark": "line"
}
DEFAULT_SUBTRACK_2D_POINT = {
    "mark": "point"
}

DEFAULT_SUBTRACK_1D_RULE = {
    "mark": "rule"
}

DEFAULT_SUBTRACK_1D_RECT = {
    "mark": "rect",
    "dataTransform": [
            {
                "type": "filter",
                "field": "Stain",
                "oneOf": ["acen"],
                "not": True
            }
    ],
    "color": {
        "field": "Stain",
        "type": "nominal",
        "domain": [
                "gneg",
                "gpos25",
                "gpos50",
                "gpos75",
                "gpos100",
                "gvar"
        ],
        "range": [
            "white",
            "#D9D9D9",
            "#979797",
            "#636363",
            "black",
            "#A0A0F2"
        ]
    }
}


DEFAULT_SUBTRACK_1D_TRIANGLERIGHT = {
    "mark": "triangleRight",
    "dataTransform": [
        {"type": "filter", "field": "Stain", "oneOf": ["acen"]},
        {"type": "filter", "field": "Name", "include": "q"}
    ],
    "color": {"value": "#B40101"}
}

DEFAULT_SUBTRACK_1D_TRIANGLELEFT = {
    "mark": "triangleLeft",
    "dataTransform": [
        {"type": "filter", "field": "Stain", "oneOf": ["acen"]},
        {"type": "filter", "field": "Name", "include": "p"}
    ],
    "color": {"value": "#B40101"}
}

DEFAULT_TRACK = {
    "width": 800,
    "height": 180,
    "data": {
        "url": "https://resgen.io/api/v1/tileset_info/?d=UvVPeLHuRDiYA3qwFlm7xQ",
        "type": "multivec",
        "row": "sample",
        "column": "position",
        "value": "peak",
        "categories": ["sample 1"],
        "binSize": 5
    },
    "layout": "linear",
    "x": {"field": "start", "type": "genomic", "axis": "bottom"},
    "xe": {"field": "end", "type": "genomic"},
    "y": {"field": "peak", "type": "quantitative", "axis": "right"},
    "row": {"field": "sample", "type": "nominal"},
    "size": {"value": 5}
}

DEFAULT_TRACK_1D = {
    "width": 800,
    "height": 40,
    "data": {
        "url": "https://raw.githubusercontent.com/sehilyi/gemini-datasets/master/data/UCSC.HG38.Human.CytoBandIdeogram.csv",
        "type": "csv",
        "chromosomeField": "Chromosome",
        "genomicFields": ["chromStart", "chromEnd"]
    },
    "x": {
        "field": "chromStart",
        "type": "genomic",
        "domain": {"chromosome": "chr1"},
        "axis": "top"
    },
    "xe": {"field": "chromEnd", "type": "genomic"},
    "size": {"value": 20},
}

DEFAULT_TRACK_HEATMAP = {
    "data": {
        "url": "https://server.gosling-lang.org/api/v1/tileset_info/?d=hffc6-microc-hg38",
        "type": "matrix"
    },
    "mark": "rect",
    "x": {"field": "xs", "type": "genomic", "axis": "none"},
    "xe": {"field": "xe", "type": "genomic", "axis": "none"},
    "y": {"field": "ys", "type": "genomic", "axis": "none"},
    "ye": {"field": "ye", "type": "genomic", "axis": "none"},
    "color": {
        "field": "value",
        "type": "quantitative",
        "range": "warm"
    },
    "width": 600,
    "height": 600
}


def get_default_track(names):
    if len(names) == 0:
        return None
    if len(names) == 1 and "heatmap" in names:
        return copy.deepcopy(DEFAULT_TRACK_HEATMAP)
    #print(names,[name in MARK_1D for name in names])
    if all(name in MARK_1D for name in names):
        return copy.deepcopy(DEFAULT_TRACK_1D)
    else:
        return copy.deepcopy(DEFAULT_TRACK)


def get_default_subtrack(name):
    if name == "bar":
        return copy.deepcopy(DEFAULT_SUBTRACK_2D_BAR)
    elif name == "area":
        return copy.deepcopy(DEFAULT_SUBTRACK_2D_AREA)
    elif name == "point":
        return copy.deepcopy(DEFAULT_SUBTRACK_2D_POINT)
    elif name == "line":
        return copy.deepcopy(DEFAULT_SUBTRACK_2D_LINE)
    elif name == "heatmap":
        return None
    elif name == "triangleLeft":
        return copy.deepcopy(DEFAULT_SUBTRACK_1D_TRIANGLELEFT)
    elif name == "triangleRight":
        return copy.deepcopy(DEFAULT_SUBTRACK_1D_TRIANGLERIGHT)
    elif name == "rule":
        return copy.deepcopy(DEFAULT_SUBTRACK_1D_RULE)
    elif name == "rect":
        return copy.deepcopy(DEFAULT_SUBTRACK_1D_RECT)
