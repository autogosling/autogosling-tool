import copy
import json
import os
import marker


EX_TRACK_INFO = [{'x': 0, 'y': 0, 'width': 400, 'height': 430, 'layout': 'linear', 'mark': 'bar'}, {'x': 0, 'y': 450, 'width': 400, 'height': 430, 'layout': 'linear', 'mark': 'line'}, {'x': 410, 'y': 0, 'width': 400,
                                                                                                                                                                                         'height': 880, 'layout': 'linear', 'mark': 'point'}, {'x': 0, 'y': 890, 'width': 800, 'height': 210, 'layout': 'linear', 'mark': 'area'}, {'x': 0, 'y': 1100, 'width': 800, 'height': 210, 'layout': 'linear', 'mark': 'line'}]

# EXTRACTED_INFO_PATH = "../data/extracted"
EXTRACTED_INFO_PATH = "/new_mem/manqing/autogosling-tool/model/data/splits/split-42-0.2-0.1/test"


def create_filenames(example):
    filenames = {
        "box": os.path.join(EXTRACTED_INFO_PATH, "bounding_box", example+".json"),
        "layout": os.path.join(EXTRACTED_INFO_PATH, "layouts", example+".json"),
        "mark": os.path.join(EXTRACTED_INFO_PATH, "chart", example+".json"),
        "orientation": os.path.join(EXTRACTED_INFO_PATH, "orientations", example+".json"),
    }
    return filenames


def read_info(filenames):
    box_infos = []
    infos = {}
    for key in filenames.keys():
        infos[key] = json.loads(open(filenames[key]).read())
    print(infos)
    for i in range(len(infos["box"])):
        new_box = {}
        for key in infos.keys():
            if key == "box":
                if "cy" in infos["box"][i].keys():
                    box = infos["box"][i]
                    new_box["x"] = box["cx"]-box["outerRadius"]
                    new_box["y"] = box["cy"]-box["outerRadius"]
                    new_box["width"] = 2*box["outerRadius"]
                    new_box["height"] = 2*box["outerRadius"]
                else:
                    new_box["x"] = infos["box"][i]["x"]
                    new_box["y"] = infos["box"][i]["y"]
                    new_box["width"] = infos["box"][i]["width"]
                    new_box["height"] = infos["box"][i]["height"]
            else:
                new_box[key] = infos[key][i]
        box_infos.append(new_box)

    return box_infos


def create_track(track_info):
    new_track = marker.get_default_track(track_info["mark"])

    new_track["layout"] = track_info["layout"]
    new_track["width"] = track_info["width"]
    new_track["height"] = track_info["height"]
    new_track["orientation"] = track_info["orientation"]
    new_track["title"] = track_info["title"]
    new_track["spacing"] = 0

    if "ideogram" in track_info["mark"]:
        return new_track
    elif "heatmap" in track_info["mark"]:
        return new_track

    new_track["tracks"] = []
    if len(track_info["mark"]) == 1:
        new_track["alignment"] = "overlay"
        new_sub_track = marker.get_default_subtrack(track_info["mark"][0])
        if new_sub_track != None:
            new_track["tracks"].append(new_sub_track)
    else:
        new_track["alignment"] = "overlay"
        
        for m in track_info["mark"]:
            new_sub_track = marker.get_default_subtrack(m)
            if new_sub_track != None:
                new_track["tracks"].append(new_sub_track)
    return new_track


def get_height(layout, curr_height, prev_height=0):
    if layout == "linear":
        return curr_height-prev_height
    elif layout == "circular":
        return (curr_height-prev_height)/2


def create_circular_stack_view(track_infos, default_center=0.3):
    new_view = {}
    new_view["alignment"] = "stack"
    new_view["layout"] = "circular"
    new_view["tracks"] = []
    sorted_infos = sorted(track_infos, key=lambda x: x["width"])
    width = sorted_infos[-1]["width"]
    x = sorted_infos[-1]["x"]
    y = sorted_infos[-1]["y"]
    prev_height = width*default_center
    for track in sorted_infos:
        new_height = track["height"]
        track["height"] = get_height(track["layout"], new_height, prev_height)
        track["width"] = width
        track["x"] = x
        track["y"] = y
        new_view["tracks"].append(create_track(track))
        prev_height = new_height
    new_view["tracks"].reverse()
    return new_view


def create_views(track_infos):
    if len(track_infos) == 1:
        return create_track(track_infos[0])
    else:
        return create_circular_stack_view(track_infos)


def get_bbox_xs(track_info):
    return track_info["x"], track_info["x"]+track_info["width"]


def get_bbox_ys(track_info):
    return track_info["y"], track_info["y"]+track_info["height"]

NUMERIC_FIELD = ["x","y", "width", "height"]
STRING_FIELD = ["orientation", "layout"]
LIST_OF_STR_FIELD = ["mark"]

def clean_track_info(track_info):
    for key, val in track_info.items():
        if key in NUMERIC_FIELD:
            track_info[key] = float(track_info[key])
        elif key in STRING_FIELD:
            if type(val) == list:
                track_info[key] = str(track_info[key][0])
        elif key in LIST_OF_STR_FIELD:
            if type(val) == str:
                track_info[key] = list(track_info[key].split(","))
    return track_info


def construct_spec(track_infos, arrangement):
    if len(track_infos) == 1:
        return create_track(track_infos[0])
    if arrangement == "vertical":
        new_arrangement = "horizontal"
        y_sorted_infos = sorted(track_infos, key=get_bbox_ys)
        all_views = []
        curr_y_high = get_bbox_ys(y_sorted_infos[0])[1]
        curr_view = [y_sorted_infos[0]]
        for info in y_sorted_infos[1:]:
            new_y_low, new_y_high = get_bbox_ys(info)
            if new_y_low >= curr_y_high-50:
                all_views.append(curr_view)
                curr_view = [info]
                curr_y_high = new_y_high
            else:
                curr_view.append(info)
                curr_y_high = max(curr_y_high, new_y_high)
        all_views.append(curr_view)
        return {
            "arrangement": arrangement,
            "views": [construct_spec(views, new_arrangement) for views in all_views]
        }
    elif arrangement == "horizontal":
        new_arrangement = "vertical"
        x_sorted_infos = sorted(track_infos, key=get_bbox_xs)
        all_views = []
        curr_x_high = get_bbox_xs(x_sorted_infos[0])[1]
        curr_view = [x_sorted_infos[0]]
        for info in x_sorted_infos[1:]:
            new_x_low, new_x_high = get_bbox_xs(info)
            if new_x_low >= curr_x_high-50:
                all_views.append(curr_view)
                curr_view = [info]
                curr_x_high = new_x_high
            else:
                curr_view.append(info)
                curr_x_high = max(curr_x_high, new_x_high)
        all_views.append(curr_view)
    if len(all_views) == 1:
        return {
            "arrangement": arrangement,
            "views": [create_views(all_views[0])]
        }
    else:
        return {
            "arrangement": arrangement,
            "views": [construct_spec(views, new_arrangement) for views in all_views]
        }


EXAMPLE_FILENAME = "complex_hierarchy_p_7_sw_1_0_s_1_2"


def generate_spec_from_example(fn=EXAMPLE_FILENAME):
    test_files = create_filenames(fn)
    info_structures = read_info(test_files)
    print(info_structures)
    spec = construct_spec(info_structures, "vertical")
    return spec


def add_track(tracks_info):
    if len(tracks_info) == 0:
        max_y = 0
        max_x = 400
        some_height = 400 
    else:
        max_y = max([track["y"]+track["height"] for track in tracks_info])
        max_x = max([track["x"]+track["width"] for track in tracks_info])
        some_height = max([track["height"] for track in tracks_info])
    new_track = {
        "x" : 0,
        "y" : max_y,
        "width": max_x,
        "height": some_height,
        "layout": "linear",
        "orientation": "horizontal",
        "spacing": 0,
        "mark": ["bar"]
    }
    tracks_info.append(new_track)
    return tracks_info

def remove_last_track(tracks_info):
    print(tracks_info)

    if len(tracks_info)>0:
        print(tracks_info)

        return tracks_info[:-1]
    return tracks_info

if __name__ == "__main__":
    res = generate_spec_from_example()
    print(json.dumps(res))
