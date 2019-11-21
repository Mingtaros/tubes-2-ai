import cv2
import Rules

def findShapes(filename, shape): # diasumsikan filename sudah ditambahkan "images/" diawal
    font = cv2.FONT_HERSHEY_COMPLEX

    img = cv2.imread(filename)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #grayscaled image to find threshold and contours
    _, threshold = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY) #change threshold to adaptive
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    shape_detector = Rules.ShapeIdentifier()
    hit_rules = []

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        # Shape Detector
        shape_detector.reset()
        shape_detector.result = []
        angles = [90, 80, 100, 90] #stub, ganti dengan list of angles yang sebenarnya
        shape_detector.declare(Rules.Fact(jumlah_sudut = len(approx), list_of_angles = angles))
        #list_of_angles dibaca secara counter-clockwise dari gambar
        shape_detector.run()

        # x dan y merupakan x dan y letak shape
        x = approx.ravel()[0]
        y = approx.ravel()[1]

        if (shape == "All Shapes"):
            #Gambar semua shape
            cv2.drawContours(img, [approx], 0, (0), 3)
            hit_rules += [x[1] for x in shape_detector.result] + ['==============================================================================']
        elif ((shape != "All Shapes") and (shape in [x[0] for x in shape_detector.result])):
            cv2.drawContours(img, [approx], 0, (0), 3)
            cv2.putText(img, shape, (x,y), font, 1, (0)) #optional, mungkin gk usah
            hit_rules += [x[1] for x in shape_detector.result] + ['==============================================================================']
        
    yield ("\n\n".join(hit_rules))
    yield img

if __name__ == "__main__":
    filename = "images/" + input("Filename: ")
    shape = input("Shape to search for: ")
    hit_rules, after = findShapes(filename, shape)
    print(hit_rules)
    cv2.imshow("after", after)
    cv2.waitKey(0) # quit with pressing 0