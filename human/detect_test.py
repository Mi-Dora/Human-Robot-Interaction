from face_detect import *

if __name__ == '__main__':
    cv2_img = cv2.imread('images/test2.jpg')
    draw_image, face_num = Local_face(cv2_img, True)
    print(face_num)
    cv2.imshow('test', draw_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()