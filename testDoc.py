from xml.dom.minidom import Document
import numpy as np
if __name__ == "__main__":
    doc = Document()
    img = np.zeros((10,10,3))
    objects = [
        ['face', 'Uspecified', 0, 0, [1, 1, 2, 2]],
        ['face2', 'Uspecified', 0, 0, [1, 1, 3, 3]],
    ]
    annotation = doc.createElement('annotation')
    doc.appendChild(annotation)
    folder = doc.createElement('folder')
    annotation.appendChild(folder)
    folder_text = doc.createTextNode('VOCType')
    folder.appendChild(folder_text)

    source = doc.createElement('source')
    annotation.appendChild(source)
    database = doc.createElement('database')
    source.appendChild(database)
    database_text = doc.createTextNode('VOC')
    database.appendChild(database_text)

    size = doc.createElement('size')
    annotation.appendChild(size)
    width = doc.createElement('width')
    height = doc.createElement('height')
    depth = doc.createElement('depth')
    size.appendChild(width)
    size.appendChild(height)
    size.appendChild(depth)
    width_text = doc.createTextNode(str(img.shape[0]))
    height_text = doc.createTextNode(str(img.shape[1]))
    depth_text = doc.createTextNode(str(img.shape[2]))
    width.appendChild(width_text)
    height.appendChild(height_text)
    depth.appendChild(depth_text)

    segmented = doc.createElement('segmented')
    segmented_text = doc.createTextNode('0')
    segmented.appendChild(segmented_text)
    annotation.appendChild(segmented)

    for o in objects:
        object = doc.createElement('object')
        annotation.appendChild(object)

        name = doc.createElement('name')
        object.appendChild(name)
        name_text = doc.createTextNode(o[0])
        name.appendChild(name_text)

        pose = doc.createElement('pose')
        pose_text = doc.createTextNode(o[1])
        object.appendChild(pose)
        pose.appendChild(pose_text)

        truncated = doc.createElement('truncated')
        truncated_text = doc.createTextNode(str(o[2]))
        object.appendChild(truncated)
        truncated.appendChild(truncated_text)

        difficult = doc.createElement('difficult')
        difficult_text = doc.createTextNode(str(o[3]))
        object.appendChild(difficult)
        difficult.appendChild(difficult_text)

        bndbox = doc.createElement('bndbox')
        object.appendChild(bndbox)
        xmin = doc.createElement('xmin')
        xmin_text = doc.createTextNode(str(o[4][0]))
        xmin.appendChild(xmin_text)
        ymin = doc.createElement('ymin')
        ymin_text = doc.createTextNode(str(o[4][1]))
        ymin.appendChild(ymin_text)
        xmax = doc.createElement('xmax')
        xmax_text = doc.createTextNode(str(o[4][2]))
        xmax.appendChild(xmax_text)
        ymax = doc.createElement('ymax')
        ymax_text = doc.createTextNode(str(o[4][3]))
        ymax.appendChild(ymax_text)

    with open('test.xml', 'wb') as f:
        f.write(doc.toprettyxml(indent='\t', encoding='utf-8'))