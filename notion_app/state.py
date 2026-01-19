import reflex as rx
from typing import List, Optional
from pydantic import BaseModel
import uuid

class Block(BaseModel):
    content: str = ""
    block_type: str = "text"  # text, heading, todo
    checked: bool = False

class Page(BaseModel):
    id: str = ""
    title: str = "Untitled"
    blocks: List[Block] = []
    created_at: str = ""

    def __init__(self, **data):
        if not data.get("id"):
            data["id"] = str(uuid.uuid4())
        if not data.get("blocks"):
            data["blocks"] = [
                Block(content="Welcome to your page!", block_type="heading"),
                Block(content="Start writing here...", block_type="text")
            ]
        if not data.get("created_at"):
            from datetime import datetime
            data["created_at"] = datetime.now().isoformat()
        super().__init__(**data)

class State(rx.State):
    # Page management
    pages: List[Page] = [
        Page(id="home", title="Home"),
        Page(id="page-1", title="Getting Started"),
        Page(id="page-2", title="My Notes")
    ]
    current_page_id: str = "home"

    # Computed properties for current page
    @rx.var
    def current_page(self) -> Page:
        """Get the current active page."""
        for page in self.pages:
            if page.id == self.current_page_id:
                return page
        return self.pages[0] if self.pages else Page()

    @rx.var
    def current_page_title(self) -> str:
        """Get current page title."""
        return self.current_page.title

    @rx.var
    def current_page_blocks(self) -> List[Block]:
        """Get current page blocks."""
        return self.current_page.blocks

    def navigate_to_page(self, page_id: str):
        """Navigate to a specific page."""
        if any(p.id == page_id for p in self.pages):
            self.current_page_id = page_id

    def create_new_page(self):
        """Create a new page and navigate to it."""
        new_page = Page()
        self.pages.append(new_page)
        self.current_page_id = new_page.id

    def update_page_title(self, title: str):
        """Update the current page title."""
        for i, page in enumerate(self.pages):
            if page.id == self.current_page_id:
                # Create updated page with new title
                updated_page = page.model_copy(update={"title": title})
                self.pages[i] = updated_page
                break

    def add_block_to_current_page(self, b_type: str):
        """Add a block to the current page."""
        for i, page in enumerate(self.pages):
            if page.id == self.current_page_id:
                # Create updated blocks list
                new_blocks = page.blocks.copy()
                new_blocks.append(Block(block_type=b_type))
                # Update page with new blocks
                updated_page = page.model_copy(update={"blocks": new_blocks})
                self.pages[i] = updated_page
                break

    def update_block_in_current_page(self, index: int, value: str):
        """Update a block in the current page."""
        for i, page in enumerate(self.pages):
            if page.id == self.current_page_id:
                if 0 <= index < len(page.blocks):
                    # Create updated blocks list
                    new_blocks = page.blocks.copy()
                    new_blocks[index] = new_blocks[index].model_copy(update={"content": value})
                    # Update page with new blocks
                    updated_page = page.model_copy(update={"blocks": new_blocks})
                    self.pages[i] = updated_page
                break

    def toggle_todo_in_current_page(self, index: int):
        """Toggle todo status in current page."""
        for i, page in enumerate(self.pages):
            if page.id == self.current_page_id:
                if 0 <= index < len(page.blocks):
                    # Create updated blocks list
                    new_blocks = page.blocks.copy()
                    current_checked = new_blocks[index].checked
                    new_blocks[index] = new_blocks[index].model_copy(update={"checked": not current_checked})
                    # Update page with new blocks
                    updated_page = page.model_copy(update={"blocks": new_blocks})
                    self.pages[i] = updated_page
                break

    def delete_page(self, page_id: str):
        """Delete a page."""
        if page_id != "home" and len(self.pages) > 1:  # Don't delete home or last page
            self.pages = [p for p in self.pages if p.id != page_id]
            if self.current_page_id == page_id:
                self.current_page_id = self.pages[0].id if self.pages else "home"