import copy 
import json
import os

DEFAULT_BAR_DATA = "https://resgen.io/api/v1/tileset_info/?d=UvVPeLHuRDiYA3qwFlm7xQ"
DEFAULT_BAR_TRACK = {
      "layout": "linear",
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
      "mark": "bar",
      "x": {"field": "start", "type": "genomic", "axis": "bottom"},
      "xe": {"field": "end", "type": "genomic"},
      "y": {"field": "peak", "type": "quantitative", "axis": "right"},
      "size": {"value": 5}
    }


EXTRACTED_INFO_PATH = "../data/extracted"
def create_filenames(example):
    filenames = {
        "box":os.path.join(EXTRACTED_INFO_PATH,"bounding_box",example+".json"),
        "layout":os.path.join(EXTRACTED_INFO_PATH,"layouts",example+".json"),
        "mark":os.path.join(EXTRACTED_INFO_PATH,"marks",example+".json")
    }
    return filenames   


def read_info(filenames):
    box_infos = []
    infos = {}
    for key in filenames.keys():
        infos[key] = json.loads(open(filenames[key]).read())
    for i in range(len(infos["box"])):
        new_box = {}
        for key in infos.keys():
            if key == "box":
                new_box["x"] = infos["box"][i]["x"]
                new_box["y"] = infos["box"][i]["y"]
                new_box["width"] = infos["box"][i]["width"]
                new_box["height"] = infos["box"][i]["height"]
            else:
                new_box[key] = infos[key][i]
        box_infos.append(new_box)

    return box_infos
def create_track(track_info):
    new_track = copy.deepcopy(DEFAULT_BAR_TRACK)
    for key in track_info.keys():
        if key != "x" and key != "y":
            new_track[key] = track_info[key]
    return new_track

def get_bbox_xs(track_info):
    return track_info["x"], track_info["x"]+track_info["width"]

def get_bbox_ys(track_info):
    return track_info["y"], track_info["y"]+track_info["height"]

def construct_spec(track_infos, arrangement):
    if len(track_infos) == 1:
        return {
            "tracks": [create_track(track_info) for track_info in track_infos]
        }
    if arrangement == "vertical":
        new_arrangement = "horizontal"
        y_sorted_infos = sorted(track_infos,key=get_bbox_ys)
        all_views = []
        curr_y_high = get_bbox_ys(y_sorted_infos[0])[1]
        curr_view = [y_sorted_infos[0]]
        for info in y_sorted_infos[1:]:
            new_y_low, new_y_high = get_bbox_ys(info)
            if new_y_low >= curr_y_high:
                all_views.append(curr_view)
                curr_view = [info]
                curr_y_high =  new_y_high
            else:
                curr_view.append(info)
                curr_y_high = max(curr_y_high,new_y_high)
        all_views.append(curr_view)
        return {
            "arrangement":arrangement,
            "views":[construct_spec(views,new_arrangement) for views in all_views]
        }
    elif arrangement == "horizontal":
        new_arrangement = "vertical"
        x_sorted_infos = sorted(track_infos,key=get_bbox_xs)
        all_views = []
        curr_x_high = get_bbox_xs(x_sorted_infos[0])[1]
        curr_view = [x_sorted_infos[0]]
        for info in x_sorted_infos[1:]:
            new_x_low, new_x_high = get_bbox_xs(info)
            if new_x_low >= curr_x_high:
                all_views.append(curr_view)
                curr_view = [info]
                curr_x_high =  new_x_high
            else:
                curr_view.append(info)
                curr_x_high = max(curr_x_high,new_x_high)
        all_views.append(curr_view)
        return {
            "arrangement":arrangement,
            "views":[construct_spec(views,new_arrangement) for views in all_views]
        }




def make_spec(track_hierarchy, track_infos):
    for v0 in track_hierarchy["views"]:
        for v1 in v0["views"]:
            for v2 in v1["views"]:
                new_tracks = []
                for t in v2["tracks"]:
                    new_tracks.append(create_track(track_infos[t]))
                v2["tracks"] = new_tracks
    return track_hierarchy

ex_track_info = {"layout":"linear",
                "mark":"line",
                "width":400,
                "height":210}

#print(assemble_views([ex_track_info]))


if __name__ == "__main__":
    test_files = create_filenames("complex_hierarchy")
    infos_structure = read_info(test_files)
    res = construct_spec(infos_structure,"vertical")
    print(json.dumps(res))


