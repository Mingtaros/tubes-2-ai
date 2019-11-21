import cv2
import Rules

def findShapes(filename, shape): # diasumsikan filename sudah ditambahkan "images/" diawal
    font = cv2.FONT_HERSHEY_COMPLEX

    img = cv2.imread(filename)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # print(contours)

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        shape_detector = Rules.ShapeIdentifier()
        shape_detector.reset()
        shape_detector.result = []
        shape_detector.declare(Rules.Fact(jumlah_sisi = len(approx)))
        shape_detector.run()
        if (shape in shape_detector.result):
            # x dan y merupakan x dan y letak shape
            x = approx.ravel()[0]
            y = approx.ravel()[1]
            cv2.drawContours(img, [approx], 0, (0), 3)
            cv2.putText(img, shape, (x,y), font, 1, (0))

        # if len(approx) == 3:
        #     cv2.putText(img, "Triangle", (x, y), font, 1, (0))
        # elif len(approx) == 4:
        #     cv2.putText(img, "Rectangle", (x, y), font, 1, (0))
        # elif len(approx) == 5:
        #     cv2.putText(img, "Pentagon", (x, y), font, 1, (0))
        # elif 6 < len(approx) < 15:
        #     cv2.putText(img, "Ellipse", (x, y), font, 1, (0))
        # else:
        #     cv2.putText(img, "Circle", (x, y), font, 1, (0))

    return img

if __name__ == "__main__":
    filename = "images/" + input("Filename: ")
    shape = input("Shape to search for: ")
    after = findShapes(filename, shape)
    cv2.imshow("after", after)
    cv2.waitKey(0) # quit with pressing 0