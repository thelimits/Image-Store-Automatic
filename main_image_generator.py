from FaceRecognize import Face


if __name__ == "__main__":
    Face.GenerateFaceDatabase(url="https://youtu.be/mTHMLl4dQpw", start=0, end=0.5).Generate()