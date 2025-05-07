# slides_service.py

import re
from google.oauth2 import service_account
from googleapiclient.discovery import build
from slide_mapping import mapping

SCOPES = ["https://www.googleapis.com/auth/presentations.readonly"]

def extract_text_from_element(element):
    """Extracts text from a page element."""
    text = ""
    if 'shape' in element:
        shape = element['shape']
        if 'text' in shape:
            for text_element in shape['text'].get('textElements', []):
                if 'textRun' in text_element:
                    text += text_element['textRun'].get('content', '')
    return text

class SlidesService:
    def __init__(self, creds_path: str, slides_url: str):
        # 1) Extract presentation ID from the URL
        m = re.search(r"/d/([A-Za-z0-9_-]+)", slides_url)
        if not m:
            raise ValueError(f"Invalid Google Slides URL: {slides_url}")
        presentation_id = m.group(1)

        # 2) Authenticate using service account JSON
        creds = service_account.Credentials.from_service_account_file(
            creds_path, scopes=SCOPES
        )
        service = build("slides", "v1", credentials=creds)

        # 3) Fetch the presentation
        presentation = (
            service.presentations()
                   .get(presentationId=presentation_id)
                   .execute()
        )
        slides = presentation.get("slides", [])

        # 4) Build objectId→index map and index→notes map
        self.notes_by_slide = {}

        for idx, slide in enumerate(slides, start=1):
            object_id = slide.get("objectId")
            if object_id:
                mapping.add_mapping(object_id, idx)

            # Get notes from slideProperties.notesPage
            notes_text = ""
            if 'slideProperties' in slide and 'notesPage' in slide['slideProperties']:
                notes_page = slide['slideProperties']['notesPage']
                if 'pageElements' in notes_page:
                    for element in notes_page['pageElements']:
                        notes_text += extract_text_from_element(element)

            # Clean up the text and store if not empty
            notes_text = ' '.join(notes_text.split())
            if notes_text:
                self.notes_by_slide[idx] = notes_text

    def load_all_notes(self) -> dict[int, str]:
        """
        Return a mapping of slide index → full speaker-notes text.
        """
        return self.notes_by_slide