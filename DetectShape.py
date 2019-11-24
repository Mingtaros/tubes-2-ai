import cv2
import Rules
import ImageProc

def findShapes(filename, shape, imgParam): # diasumsikan filename sudah ditambahkan "images/" diawal
    img = cv2.imread(filename)
    indexed_angles = ImageProc.process(img, imgParam[0], imgParam[1], imgParam[2], imgParam[3], imgParam[4])

    shape_detector = Rules.ShapeIdentifier()

    shape_idx = []
    hit_rules = []
    hit_facts = []

    for img_idx, angles in indexed_angles:
        #Shape Detector
        shape_detector.reset()
        shape_detector.result = []
        shape_detector.declare(Rules.Fact(jumlah_sudut = len(angles), list_of_angles = angles))
        shape_detector.run()

        if (shape == "All Shapes") or ((shape != "All Shapes") and (shape in [x[0] for x in shape_detector.result])):
            hit_rules += [x[1] for x in shape_detector.result] + ['\n========================================']
            shape_idx.append(img_idx)
            hit_facts.append((img_idx, angles))

    yield ("\n".join(hit_rules))
    yield ("\n".join([str(x) + " | " + str(y) for x, y in hit_facts]))

    for i in shape_idx:
        img = ImageProc.gambarContour(img, i)

    yield img

