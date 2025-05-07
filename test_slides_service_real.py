# test_slides_service_real.py
# test_slides_service_real.py
from slides_service import SlidesService

def test_load_notes():
    svc = SlidesService(
        "google_credentials.json",
        "https://docs.google.com/presentation/d/1xuummHZlSFguhZowJOneJqxI_ydYGBULOgdqWubVqb4/edit"
    )
    notes = svc.load_all_notes()
    # Verify we got at least slide 1
    assert 1 in notes, "Slide 1 not found in notes_by_slide"
    # Verify that the notes text is non-empty
    assert isinstance(notes[1], str) and notes[1].strip(), "Slide 1 notes are empty"

if __name__ == "__main__":
    test_load_notes()
    print("SlidesService real implementation works!")