# slide_mapping.py

class SlideMapping:
    def __init__(self):
        self.id_to_index = {}
        self.current_slide_id = None
        self.current_slide_index = 1

    def add_mapping(self, slide_id: str, index: int):
        """Add a mapping from slide ID to index."""
        self.id_to_index[slide_id] = index

    def update_current_slide(self, slide_id: str) -> int:
        """Update the current slide ID and return its index."""
        self.current_slide_id = slide_id
        self.current_slide_index = self.id_to_index.get(slide_id, 1)
        return self.current_slide_index

# Global instance
mapping = SlideMapping() 