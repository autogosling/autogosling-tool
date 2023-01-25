import os
import PIL
import PIL.Image
from PIL import Image
import json
from os.path import join as pjoin
DIR = '/home/ec2-user/data/extracted-1'

def find_matching_files(filename):
    def read_json_fn(json_fn):
        complete_fn = pjoin(DIR,json_fn,filename+".json")
        if not os.path.exists(complete_fn):
            return None
        with open(complete_fn,"r") as f:
            # import ipdb; ipdb.set_trace()
            text = f.read()
            print(text)
            return json.loads(text)
    def read_png_fn(png_fn):
        complete_path = pjoin(DIR,png_fn,filename+".png")
        if not os.path.exists(complete_path):
            return None
        pil_image =  Image.open(complete_path)
        if not pil_image.mode == 'RGB':
            pil_image = pil_image.convert('RGB')
        return pil_image 
    json_fns = ['bounding_box','layouts','chart','orientations']
    png_fns = ['screenshot']
    json_objs = [read_json_fn(json_fn) for json_fn in json_fns]
    pngs = [read_png_fn(png_fn) for png_fn in png_fns]
    if None in json_objs or None in pngs:
        return None

    def clean(bbox_el):
        if "cx" in bbox_el:
            cx,cy, d = bbox_el['cx'], bbox_el['cy'], bbox_el['outerRadius'] * 2
            w = h = d
            x = cx - w / 2
            y = cy - h / 2
            return {"x" : x, "y" : y, "width" : w, "height" : h}
        else:
            return bbox_el
    bbox, layout, chart, orientation = json_objs
    screenshot = pngs[0]
    tracks_info = [{**clean(bbox_el),"layout" : layout_el, "mark" : chart_el, "orientation" : [orientation_el], 'score' : 1, 'layout_score' : 1} for bbox_el, layout_el, chart_el, orientation_el in zip(bbox,layout,chart,orientation)]
    return screenshot, tracks_info

if __name__ == "__main__":
    fn = "complex_hierarchy_m_0_sw_1_0_s_0_7"
    find_matching_files(fn)



