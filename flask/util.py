import itertools
def parse_list(info_tuple):
    name,x0,y0,x1,y1,cls_id,score = info_tuple
    mydict = {'x' : x0, 'y' : y0, 'width' : x1-x0, 'height' : y1-y0, 'class' : name, 'score' : score}
    return mydict

def has_iou(item1,item2,thresh=0.75):
    x0, y0, x1, y1 = item1['x'], item1['y'], item1['x'] + item1['width'], item1['y'] + item1['height']
    x2_0, y2_0, x2_1, y2_1 = item2['x'], item2['y'], item2['x'] + item2['width'], item2['y'] + item2['height']
    inner_x0 = max(x0,x2_0)
    inner_y0 = max(y0,y2_0)

    inner_x1 = min(x1,x2_1)
    inner_y1 = min(y1,y2_1)
    if inner_x0 < inner_x1 and inner_y0 < inner_y1:
        inner_area = (inner_y1 - inner_y0) * (inner_x1 - inner_x0)
        original_area = (x1-x0) * (y1 - y0)
        original_area2 = (x2_1-x2_0) * (y2_1 - y2_0)
        total_area = original_area + original_area2 - inner_area
        print(inner_area / total_area)
        if inner_area / total_area > thresh:
            # merge the two bounding boxes!
            return True
    else:
        return False

# for layout, choose the one with highest score
# for marks, output those that are > than a certain confidence score
# If only one mark in the bounding box: {'x': 0, 'y': 1100, 'width': 800, 'height': 210, 'layout': 'linear', 'mark': 'line'}
# If multiple marks in the bounding box: {'x': 0, 'y': 1100, 'width': 800, 'height': 210, 'layout': 'linear', 'mark': ['rect', 'brush']}
# TODO: Output confidence score for each prediction

def helper_cluster_similar_boxes(box,clusters):
    new_boxes = []
    found_box = False
    for cluster in clusters:
        copy_cluster = cluster.copy()
        if has_iou(cluster[0],box):
            found_box = True
            copy_cluster.append(box)
        new_boxes.append(copy_cluster)
    if not found_box:
        new_boxes.append([box])
    return new_boxes

def cluster_similar_boxes(boxes):
    clusters = []
    for box in boxes:
        clusters = helper_cluster_similar_boxes(box,clusters)
    return clusters

marker_classes = ["area", "bar", "betweenLink", "circular", "heatmap", "ideogram", "line", "point", "rect", "rule", "text", "triangleLeft", "triangleRight", "withinLink"]

# Selects all labels from a given category that have a confidence score that is greater than a certain threshold
def merge_identical_boxes(all_boxes,threshold=0.7):
    print(all_boxes)
    clusters = cluster_similar_boxes(all_boxes)
    def merge_labels(boxes):
        initial_obj = boxes[0].copy()
        #all_classes = [box['class'] for box in boxes if box['score'] > threshold]
        print([box['class'] for box in boxes])
        
        marker_boxes= [box for box in boxes if box["class"] in marker_classes]
        if len(marker_boxes)>0:
            best_marker_score = max([box["score"] for box in marker_boxes])
            best_orient = max([box for box in boxes if box['class'] not in marker_classes], key = lambda x:x["score"])
            all_classes = [best_orient["class"]]+[box["class"] for box in marker_boxes if box['score']>threshold*best_marker_score]
            all_scores = [best_orient["score"]]+[box["score"] for box in marker_boxes if box['score']>threshold*best_marker_score]
        else:
            all_classes = []
            all_scores = []
        print(all_classes)
        if "ideogram" in all_classes:
            all_classes = ["ideogram"]
        elif "heatmap" in all_classes:
            all_classes = ["heatmap"]
        initial_obj['class'] = [c for c in all_classes if c is not 'circular' and c is not 'linear']
        initial_obj['score'] = all_scores
        print(initial_obj)
        return initial_obj
    result = [merge_labels(cluster) for cluster in clusters]
    print(result)
    return result

# Selects only the best layout from similar bounding boxes
def select_best_from_identical_boxes(all_boxes):
    clusters = cluster_similar_boxes(all_boxes)
    def merge_cluster(cluster):
        return max([box for box in cluster],key=lambda el: el['score'])
    return [merge_cluster(cluster) for cluster in clusters]

def merge_parsed_list(shape_list,prop_list):
    merged_list = []
    for item1, item2 in itertools.product(shape_list,prop_list):
        if has_iou(item1,item2,thresh=0.6):
            new_item = {'x' : float(item1['x']), 'y' : float(item1['y']), 'width' : float(item1['width']), 'height' : float(item1['height']), 'layout' : item1['class'], 'mark' : item2['class'], 'layout_score' : item1['score'], 'score' : item2['score']}
            merged_list.append(new_item)
    return merged_list