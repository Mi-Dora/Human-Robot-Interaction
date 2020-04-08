import face_recognition

def face_compare(unknow_person_img):
    known_person_1 = face_recognition.load_image_file("images/obama.jpg")
    known_person_2 = face_recognition.load_image_file("images/biden.jpg")

    known_person_1_encoding = face_recognition.face_encodings(known_person_1)[0]
    known_person_2_encoding = face_recognition.face_encodings(known_person_2)[0]

    known_encodings = [
        known_person_1_encoding,
        known_person_2_encoding
    ]

    # when people come in one by one, take a photo and test it
    unknown_person_encoding = face_recognition.face_encodings(unknow_person_img)[0]

    # See how far apart the test image is from the known faces
    face_distances = face_recognition.face_distance(known_encodings, unknown_person_encoding)

    for i, face_distance in enumerate(face_distances):
        print("The test image has a distance of {:.2} from known image #{}".format(face_distance, i + 1))
        print("- With a normal cutoff of 0.6, would the test image match the known image? {}".format(face_distance < 0.6))
        print("- With a very strict cutoff of 0.5, would the test image match the known image? {}".format(face_distance < 0.5))
