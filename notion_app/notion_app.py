import reflex as rx
from .state import State, Block

def render_block(block: Block, index: int):
    """Renders an individual content block based on its type with Notion-like styling."""
    return rx.hstack(
        # Conditional Checkbox for Todo types
        rx.cond(
            block.block_type == "todo",
            rx.checkbox(
                is_checked=block.checked,
                on_change=lambda _: State.toggle_todo_in_current_page(index),
                color_scheme="indigo",
                class_name="mt-1 mr-2 flex-shrink-0"
            ),
        ),
        # Editable text area for all blocks
        rx.input(
            value=block.content,
            on_change=lambda v: State.update_block_in_current_page(index, v),
            class_name=rx.cond(
                block.block_type == "heading",
                "text-xl font-bold bg-transparent border-none outline-none focus:ring-0 w-full py-1 px-2 hover:bg-gray-50 rounded transition-colors",
                "text-base bg-transparent border-none outline-none focus:ring-0 w-full py-1 px-2 hover:bg-gray-50 rounded transition-colors"
            ),
            placeholder="Type something...",
            text_decoration=rx.cond(
                (block.block_type == "todo") & block.checked,
                "line-through",
                "none"
            ),
        ),
        class_name="w-full group",
        spacing="2",
        align="start",
    )

def sidebar():
    """Left navigation sidebar with dynamic pages."""
    return rx.box(
        rx.vstack(
            # Logo/Brand
            rx.hstack(
                rx.box(
                    class_name="w-8 h-8 bg-gray-900 rounded-md flex items-center justify-center mr-3"
                ),
                rx.heading(
                    "Notion",
                    class_name="text-lg font-semibold text-gray-900"
                ),
                class_name="mb-6"
            ),

            # Workspace section
            rx.text(
                "Workspace",
                class_name="text-xs font-medium text-gray-500 uppercase tracking-wider mb-2"
            ),

            # Dynamic page list
            rx.vstack(
                rx.foreach(
                    State.pages,
                    lambda page: rx.button(
                        rx.hstack(
                            rx.cond(
                                page.id == "home",
                                rx.text("🏠", class_name="mr-2"),
                                rx.text("📄", class_name="mr-2")
                            ),
                            rx.text(page.title, class_name="truncate"),
                            class_name="flex-1 text-left"
                        ),
                        on_click=lambda: State.navigate_to_page(page.id),
                        class_name=rx.cond(
                            State.current_page_id == page.id,
                            "w-full justify-start px-3 py-2 text-sm font-medium text-gray-900 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors",
                            "w-full justify-start px-3 py-2 text-sm font-medium text-gray-700 bg-transparent rounded-md hover:bg-gray-100 transition-colors"
                        ),
                        variant="ghost",
                    )
                ),
                class_name="space-y-1 mb-4"
            ),

            # New page button
            rx.button(
                rx.hstack(
                    rx.text("➕", class_name="mr-2"),
                    rx.text("New page", class_name="flex-1 text-left"),
                    class_name="w-full"
                ),
                on_click=State.create_new_page,
                class_name="w-full justify-start px-3 py-2 text-sm font-medium text-gray-700 bg-transparent rounded-md hover:bg-gray-100 border border-gray-200 transition-colors",
                variant="outline",
            ),

            class_name="flex-1"
        ),
        class_name="w-64 h-screen bg-white border-r border-gray-200 p-4 flex flex-col"
    )

def editor():
    """Main editing canvas with Notion-like styling."""
    return rx.box(
        rx.vstack(
            # Page Title Input
            rx.input(
                value=State.current_page_title,
                on_change=State.update_page_title,
                class_name="text-4xl font-bold bg-transparent border-none outline-none focus:ring-0 w-full mb-8 placeholder-gray-400",
                placeholder="Untitled",
            ),

            # Dynamic Block List
            rx.vstack(
                rx.foreach(
                    State.current_page_blocks,
                    lambda block, index: render_block(block, index)
                ),
                class_name="w-full space-y-1 mb-8"
            ),

            # Add Block Toolbar
            rx.hstack(
                rx.button(
                    rx.hstack(
                        rx.text("＋", class_name="mr-1"),
                        rx.text("Text"),
                    ),
                    on_click=lambda: State.add_block_to_current_page("text"),
                    class_name="px-3 py-1.5 text-sm font-medium text-gray-700 bg-gray-100 rounded hover:bg-gray-200 transition-colors opacity-60 hover:opacity-100"
                ),
                rx.button(
                    rx.hstack(
                        rx.text("＋", class_name="mr-1"),
                        rx.text("Heading"),
                    ),
                    on_click=lambda: State.add_block_to_current_page("heading"),
                    class_name="px-3 py-1.5 text-sm font-medium text-gray-700 bg-gray-100 rounded hover:bg-gray-200 transition-colors opacity-60 hover:opacity-100"
                ),
                rx.button(
                    rx.hstack(
                        rx.text("＋", class_name="mr-1"),
                        rx.text("To-do"),
                    ),
                    on_click=lambda: State.add_block_to_current_page("todo"),
                    class_name="px-3 py-1.5 text-sm font-medium text-gray-700 bg-gray-100 rounded hover:bg-gray-200 transition-colors opacity-60 hover:opacity-100"
                ),
                class_name="space-x-2"
            ),

            class_name="flex-1"
        ),
        class_name="flex-1 max-w-4xl mx-auto px-8 py-12"
    )

def page_component():
    """Main page component that combines sidebar and editor."""
    return rx.hstack(
        sidebar(),
        rx.box(
            editor(),
            class_name="flex-1 bg-white overflow-y-auto"
        ),
        class_name="h-screen bg-gray-50"
    )

# Create the app with Tailwind CSS
app = rx.App(
    theme=rx.theme(
        appearance="light",
        has_background=True,
        radius="medium",
        accent_color="gray",
    ),
    style={
        "font_family": "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
    }
)

# Add the main page
app.add_page(page_component, route="/", title="Notion Clone")