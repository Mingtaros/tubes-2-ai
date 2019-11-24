import cv2
import Rules
import ImageProc

def findShapes(filename, shape, imgParam): # diasumsikan filename sudah ditambahkan "images/" diawal
    img = cv2.imread(filename)
    indexed_angles = ImageProc.process(img, imgParam[0], imgParam[1], imgParam[2], imgParam[3], imgParam[4])

    shape_detector = Rules.ShapeIdentifier()

    shape_idx = []
    hit_rules = []

    for img_idx, angles in indexed_angles:
        #Shape Detector
        shape_detector.reset()
        shape_detector.result = []
        shape_detector.declare(Rules.Fact(jumlah_sudut = len(angles), list_of_angles = angles))
        shape_detector.run()

        if (shape == "All Shapes") or ((shape != "All Shapes") and (shape in [x[0] for x in shape_detector.result])):
            print(img_idx, angles)
            hit_rules += [str(img_idx)] + [x[1] for x in shape_detector.result] + ['==============================================================================']
            shape_idx.append(img_idx)

    yield shape_idx
    yield ("\n\n".join(hit_rules))

    for i in shape_idx:
        img = ImageProc.gambarContour(img, i)

    yield img

# if __name__ == "__main__":
#     filename = "images/" + "test_shape.jpg"#input("Filename: ")
#     shape = input("Shape to search for: ")
#     shape_idx, hit_rules, after = findShapes(filename, shape)
#     print(hit_rules)
#     print(shape_idx)
#     for i in shape_idx:
#         after = ImageProc.gambarContour(after, i)
#     ImageProc.show(after, "WOW")
