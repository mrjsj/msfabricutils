# Go to https://learn.microsoft.com/en-us/rest/api/fabric/core/external-data-shares/list-external-data-shares-in-item?tabs=HTTP

Run this in console

```js
// Find all tree expander elements that are collapsed (not expanded)
function expandAll() {
    // Keep expanding until no more collapsed items are found
    const findAndExpandCollapsed = () => {
        // Find tree items that aren't expanded
        const collapsedItems = document.querySelectorAll('.tree-item:not(.is-expanded) > .tree-expander');
        
        if (collapsedItems.length > 0) {
            // Click each collapsed item
            collapsedItems.forEach(item => item.click());
            
            // Check again after a short delay to allow for any animations/loading
            setTimeout(findAndExpandCollapsed, 100);
        }
    };

    findAndExpandCollapsed();
}

// Run the function
expandAll();
```

Open inspector and copy the nav element into `navbar.html`

Run extract_nav.py


https://github.com/Azure/azure-cli/blob/dev/doc/command_guidelines.md