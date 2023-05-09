import copy

MARK_1D = ["rect", "triangleLeft", "triangleRight",
           "rule", "betweenLink", "withinLink"]
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



DEFAULT_SUBTRACK_1D_RECT =  {
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
                "gpos25"
        ],
        "range": [
            "white",
            "#A0A0F2"
        ]
    }
}


DEFAULT_SUBTRACK_1D_IDEOGRAM = {
          "alignment": "overlay",
          "data": {
            "url": "https://raw.githubusercontent.com/sehilyi/gemini-datasets/master/data/cytogenetic_band.csv",
            "type": "csv",
            "chromosomeField": "Chr.",
            "genomicFields": [
              "ISCN_start",
              "ISCN_stop",
              "Basepair_start",
              "Basepair_stop"
            ]
          },
          "tracks": [
            {
              "mark": "rect",
              "dataTransform": [
                {
                  "type": "filter",
                  "field": "Stain",
                  "oneOf": ["acen-1", "acen-2"],
                  "not": True
                }
              ],
              "color": {
                "field": "Density",
                "type": "nominal",
                "domain": ["", "25", "50", "75", "100"],
                "range": ["white", "#D9D9D9", "#979797", "#636363", "black"]
              },
              "size": {"value": 20}
            },
            {
              "mark": "rect",
              "dataTransform": [
                {"type": "filter", "field": "Stain", "oneOf": ["gvar"]}
              ],
              "color": {"value": "#A0A0F2"},
              "size": {"value": 20}
            },
            {
              "mark": "triangleRight",
              "dataTransform": [
                {"type": "filter", "field": "Stain", "oneOf": ["acen-1"]}
              ],
              "color": {"value": "#B40101"},
              "size": {"value": 20}
            },
            {
              "mark": "triangleLeft",
              "dataTransform": [
                {"type": "filter", "field": "Stain", "oneOf": ["acen-2"]}
              ],
              "color": {"value": "#B40101"},
              "size": {"value": 20}
            }
          ],
          "x": {"field": "Basepair_start", "type": "genomic", "axis": "none", "domain":{"interval":[100000000,300000000]}},
          "xe": {"field": "Basepair_stop", "type": "genomic"},
          "stroke": {"value": "black"},
          "strokeWidth": {"value": 1},
          "style": {"outlineWidth": 0},
          "width": 200,
          "height": 250
        }


DEFAULT_SUBTRACK_1D_TRIANGLERIGHT = {
            "dataTransform": [
              {"type": "filter", "field": "type", "oneOf": ["gene"]},
              {"type": "filter", "field": "strand", "oneOf": ["+"]}
            ],
            "mark": "triangleRight",
            "x": {"field": "end", "type": "genomic", "axis": "none"},
            "size": {"value": 15}
          }

DEFAULT_SUBTRACK_1D_TRIANGLELEFT = {
            "dataTransform": [
              {"type": "filter", "field": "type", "oneOf": ["gene"]},
              {"type": "filter", "field": "strand", "oneOf": ["-"]}
            ],
            "mark": "triangleLeft",
            "x": {"field": "start", "type": "genomic", "axis": "none"},
            "size": {"value": 15},
            "style": {"align": "right"}
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
    "x": {"field": "start", "type": "genomic", "axis": "none"},
    "xe": {"field": "end", "type": "genomic"},
    "y": {"field": "peak", "type": "quantitative", "axis": "none"},
    "row": {"field": "sample", "type": "nominal"},
    "size": {"value": 5},
    "color":{"range": ["#E79F00"],
             "field":"sample",
              "type": "nominal",},
    "opacity":{"value":1},
    "style": {"outlineWidth":0},
}

DEFAULT_TRACK_1D = {
        "data": {
          "url": "https://server.gosling-lang.org/api/v1/tileset_info/?d=gene-annotation",
          "type": "beddb",
          "genomicFields": [
            {"index": 1, "name": "start"},
            {"index": 2, "name": "end"}
          ],
          "valueFields": [
            {"index": 5, "name": "strand", "type": "nominal"},
            {"index": 3, "name": "name", "type": "nominal"}
          ],
          "exonIntervalFields": [
            {"index": 12, "name": "start"},
            {"index": 13, "name": "end"}
          ]
        },
        "color": {
          "value":"#7585FF"
        },
        "opacity": {"value": 1},
        "width": 350,
        "height": 100,
        "style": {"outlineWidth":1}
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
    if "ideogram" in names:
        return copy.deepcopy(DEFAULT_SUBTRACK_1D_IDEOGRAM)
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


