// ARIA attributes and utilities for accessibility

// ARIA roles for different component types
export const ARIA_ROLES = {
  // Landmark roles
  banner: 'banner',
  complementary: 'complementary',
  contentinfo: 'contentinfo',
  form: 'form',
  main: 'main',
  navigation: 'navigation',
  region: 'region',
  search: 'search',

  // Widget roles
  button: 'button',
  checkbox: 'checkbox',
  combobox: 'combobox',
  grid: 'grid',
  gridcell: 'gridcell',
  listbox: 'listbox',
  listitem: 'listitem',
  menu: 'menu',
  menubar: 'menubar',
  menuitem: 'menuitem',
  menuitemcheckbox: 'menuitemcheckbox',
  menuitemradio: 'menuitemradio',
  option: 'option',
  radiogroup: 'radiogroup',
  radio: 'radio',
  scrollbar: 'scrollbar',
  searchbox: 'searchbox',
  slider: 'slider',
  spinbutton: 'spinbutton',
  switch: 'switch',
  tab: 'tab',
  tablist: 'tablist',
  tabpanel: 'tabpanel',
  textbox: 'textbox',
  tooltip: 'tooltip',
  tree: 'tree',
  treeitem: 'treeitem',

  // Document structure roles
  article: 'article',
  cell: 'cell',
  columnheader: 'columnheader',
  definition: 'definition',
  directory: 'directory',
  document: 'document',
  feed: 'feed',
  figure: 'figure',
  group: 'group',
  heading: 'heading',
  img: 'img',
  list: 'list',
  math: 'math',
  note: 'note',
  presentation: 'presentation',
  row: 'row',
  rowgroup: 'rowgroup',
  rowheader: 'rowheader',
  separator: 'separator',
  table: 'table',
  term: 'term',

  // Live region roles
  alert: 'alert',
  log: 'log',
  marquee: 'marquee',
  status: 'status',
  timer: 'timer',

  // Window roles
  alertdialog: 'alertdialog',
  dialog: 'dialog',
} as const

// ARIA attributes interface
export interface AriaAttributes {
  // Labeling relationships
  'aria-label'?: string
  'aria-labelledby'?: string
  'aria-describedby'?: string
  'aria-details'?: string

  // Properties and states
  'aria-checked'?: boolean | 'mixed'
  'aria-disabled'?: boolean
  'aria-expanded'?: boolean
  'aria-haspopup'?: boolean | 'menu' | 'listbox' | 'tree' | 'grid' | 'dialog'
  'aria-hidden'?: boolean
  'aria-invalid'?: boolean | 'grammar' | 'spelling'
  'aria-pressed'?: boolean | 'mixed'
  'aria-selected'?: boolean
  'aria-current'?: boolean | 'page' | 'step' | 'location' | 'date' | 'time'
  'aria-sort'?: 'ascending' | 'descending' | 'none' | 'other'
  'aria-orientation'?: 'horizontal' | 'vertical'

  // Drag and drop
  'aria-dropeffect'?: 'copy' | 'execute' | 'link' | 'move' | 'none' | 'popup'
  'aria-grabbed'?: boolean | 'false' | 'true'

  // Relationship attributes
  'aria-owns'?: string
  'aria-posinset'?: number
  'aria-setsize'?: number
  'aria-level'?: number
  'aria-multiselectable'?: boolean
  'aria-required'?: boolean
  'aria-readonly'?: boolean
  'aria-atomic'?: boolean
  'aria-busy'?: boolean
  'aria-live'?: 'off' | 'polite' | 'assertive'
  'aria-relevant'?: 'additions' | 'removals' | 'text' | 'all'
  'aria-valuemax'?: number
  'aria-valuemin'?: number
  'aria-valuenow'?: number
  'aria-valuetext'?: string
}

// Common ARIA attribute sets for different component types
export const ARIA_ATTRIBUTES = {
  // For buttons
  button: {
    role: 'button',
    'aria-pressed': undefined, // Only set if it's a toggle button
  } as AriaAttributes,

  // For checkboxes
  checkbox: {
    role: 'checkbox',
    'aria-checked': false,
  } as AriaAttributes,

  // For radio buttons
  radio: {
    role: 'radio',
    'aria-checked': false,
  } as AriaAttributes,

  // For tabs
  tab: {
    role: 'tab',
    'aria-selected': false,
    'aria-controls': undefined, // ID of associated panel
    'aria-setsize': undefined, // Total number of tabs
    'aria-posinset': undefined, // Position of tab in set
  } as AriaAttributes,

  // For tab panels
  tabPanel: {
    role: 'tabpanel',
    'aria-labelledby': undefined, // ID of associated tab
  } as AriaAttributes,

  // For modal dialogs
  modal: {
    role: 'dialog',
    'aria-modal': true,
    'aria-labelledby': undefined, // ID of title element
    'aria-describedby': undefined, // ID of description element
  } as AriaAttributes,

  // For alerts
  alert: {
    role: 'alert',
    'aria-live': 'assertive',
  } as AriaAttributes,

  // For status messages
  status: {
    role: 'status',
    'aria-live': 'polite',
    'aria-atomic': true,
  } as AriaAttributes,

  // For progress bars
  progressbar: {
    role: 'progressbar',
    'aria-valuemin': 0,
    'aria-valuemax': 100,
    'aria-valuenow': undefined, // Current value
    'aria-valuetext': undefined, // Human-readable value
  } as AriaAttributes,

  // For sliders
  slider: {
    role: 'slider',
    'aria-valuemin': 0,
    'aria-valuemax': 100,
    'aria-valuenow': undefined, // Current value
    'aria-orientation': 'horizontal',
  } as AriaAttributes,

  // For comboboxes
  combobox: {
    role: 'combobox',
    'aria-expanded': false,
    'aria-haspopup': 'listbox',
    'aria-autocomplete': 'list',
    'aria-controls': undefined, // ID of listbox
  } as AriaAttributes,

  // For listboxes
  listbox: {
    role: 'listbox',
    'aria-multiselectable': false,
  } as AriaAttributes,

  // For list items
  listitem: {
    role: 'listitem',
    'aria-selected': undefined, // Only for selectable list items
    'aria-setsize': undefined, // Total number of items
    'aria-posinset': undefined, // Position of item in set
  } as AriaAttributes,

  // For trees
  tree: {
    role: 'tree',
  } as AriaAttributes,

  // For tree items
  treeitem: {
    role: 'treeitem',
    'aria-expanded': undefined, // Only if the item has children
    'aria-level': undefined, // Nesting level
    'aria-setsize': undefined, // Number of items at this level
    'aria-posinset': undefined, // Position among items at this level
  } as AriaAttributes,

  // For grids
  grid: {
    role: 'grid',
    'aria-readonly': true,
  } as AriaAttributes,

  // For grid cells
  gridcell: {
    role: 'gridcell',
    'aria-readonly': undefined, // Whether the cell is read-only
  } as AriaAttributes,
}

// Utility function to generate ARIA attributes for a component
export function getAriaAttributes(componentType: keyof typeof ARIA_ATTRIBUTES, overrides?: AriaAttributes): AriaAttributes {
  return {
    ...ARIA_ATTRIBUTES[componentType],
    ...overrides,
  }
}

// Utility function to check if an element has focusable descendants
export function hasFocusableDescendants(element: HTMLElement): boolean {
  const focusableElements = element.querySelectorAll(
    'a[href], button, input, select, textarea, [tabindex]:not([tabindex="-1"])'
  )
  return focusableElements.length > 0
}

// Utility function to generate unique IDs for ARIA relationships
let idCounter = 0
export function generateId(prefix: string = 'aria'): string {
  idCounter++
  return `${prefix}-${idCounter}`
}

// Utility function to manage ARIA attributes for dynamic components
export interface AriaManager {
  updateAriaAttribute: (attribute: keyof AriaAttributes, value: any) => void
  removeAriaAttribute: (attribute: keyof AriaAttributes) => void
  getAriaAttribute: (attribute: keyof AriaAttributes) => any
  getAllAriaAttributes: () => AriaAttributes
}

export function createAriaManager(initialAttributes: AriaAttributes = {}): AriaManager {
  let attributes = { ...initialAttributes }

  return {
    updateAriaAttribute(attribute, value) {
      attributes = {
        ...attributes,
        [attribute]: value,
      }
    },

    removeAriaAttribute(attribute) {
      const { [attribute]: _, ...rest } = attributes
      attributes = rest
    },

    getAriaAttribute(attribute) {
      return attributes[attribute]
    },

    getAllAriaAttributes() {
      return { ...attributes }
    },
  }
}

// Utility function to manage ARIA live regions
export function announceToScreenReader(message: string, politeness: 'polite' | 'assertive' = 'polite'): void {
  // Create a temporary element for screen reader announcements
  const announcement = document.createElement('div')

  // Apply ARIA live attributes
  announcement.setAttribute('aria-live', politeness)
  announcement.setAttribute('aria-atomic', 'true')
  announcement.className = 'sr-only' // Visually hidden but accessible to screen readers
  announcement.textContent = message

  // Add to document body
  document.body.appendChild(announcement)

  // Remove after a delay to prevent clutter
  setTimeout(() => {
    document.body.removeChild(announcement)
  }, 1000)
}

// Utility function to manage ARIA-describedBy relationships
export function createDescribedByRelation(descriptionId: string, targetElement: HTMLElement): () => void {
  // Add the aria-describedby attribute to the target element
  const originalDescribedBy = targetElement.getAttribute('aria-describedby')
  const newDescribedBy = originalDescribedBy
    ? `${originalDescribedBy} ${descriptionId}`
    : descriptionId

  targetElement.setAttribute('aria-describedby', newDescribedBy)

  // Return a cleanup function
  return () => {
    const currentDescribedBy = targetElement.getAttribute('aria-describedby')
    if (currentDescribedBy) {
      const updatedDescribedBy = currentDescribedBy
        .split(' ')
        .filter(id => id !== descriptionId)
        .join(' ')

      if (updatedDescribedBy) {
        targetElement.setAttribute('aria-describedby', updatedDescribedBy)
      } else {
        targetElement.removeAttribute('aria-describedby')
      }
    }
  }
}

// Utility function to manage ARIA-labelledby relationships
export function createLabelledByRelation(labelId: string, targetElement: HTMLElement): () => void {
  // Add the aria-labelledby attribute to the target element
  const originalLabelledBy = targetElement.getAttribute('aria-labelledby')
  const newLabelledBy = originalLabelledBy
    ? `${originalLabelledBy} ${labelId}`
    : labelId

  targetElement.setAttribute('aria-labelledby', newLabelledBy)

  // Return a cleanup function
  return () => {
    const currentLabelledBy = targetElement.getAttribute('aria-labelledby')
    if (currentLabelledBy) {
      const updatedLabelledBy = currentLabelledBy
        .split(' ')
        .filter(id => id !== labelId)
        .join(' ')

      if (updatedLabelledBy) {
        targetElement.setAttribute('aria-labelledby', updatedLabelledBy)
      } else {
        targetElement.removeAttribute('aria-labelledby')
      }
    }
  }
}

// Utility function to manage ARIA controls relationships
export function createControlsRelation(controlledId: string, controllerElement: HTMLElement): () => void {
  // Add the aria-controls attribute to the controller element
  const originalControls = controllerElement.getAttribute('aria-controls')
  const newControls = originalControls
    ? `${originalControls} ${controlledId}`
    : controlledId

  controllerElement.setAttribute('aria-controls', newControls)

  // Return a cleanup function
  return () => {
    const currentControls = controllerElement.getAttribute('aria-controls')
    if (currentControls) {
      const updatedControls = currentControls
        .split(' ')
        .filter(id => id !== controlledId)
        .join(' ')

      if (updatedControls) {
        controllerElement.setAttribute('aria-controls', updatedControls)
      } else {
        controllerElement.removeAttribute('aria-controls')
      }
    }
  }
}