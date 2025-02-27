# 📝 MisterLister

Welcome to **MisterLister**! Born from my _**P**ersonal **A**pp **C**reation **I**nitiative_ (fancy name for a hobby project 🤓), this is a clean, minimalist table editor that turns your filenames into formatted, printable lists.

## 🎯 Purpose & Scope

MisterLister started as my personal solution for a very specific need: turning Windows filenames into organized, printable lists without the usual hassles. While it's currently tailored to my particular workflow and filename formatting preferences, it's built with love and an eye toward future expansion.

It is not a general-purpose tool (at the moment), it only works with filenames that follow a strict structure:

```LastName FirstName DateOfBirth Item ItemDate```

If your files don't match this format, the program will not function as expected. While it is tailored to my personal workflow, others may find it useful with modifications.

## 💡 Features

- Clean, distraction-free interface for working with filename lists
- Customizable font size and row spacing for your filename displays
- Print preview and export capabilities for your filename lists
- Window size/position memory (it remembers where you like things)
- Configurable border styles for printing your lists
- Drag and drop support for easy filename importing

## 🚀 Getting Started

### You'll Need
- Python 3.8 or higher
- PyQt6
- A desire for easy filename printing

### Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/MisterLister.git
cd MisterLister
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python -m mister_lister
```

## 🛠️ Make It Your Own
Want to adapt MisterLister for your own file naming conventions or add features specific to your workflow? Check out the [Customization Guide](CUSTOMIZATION.md) for detailed examples of how to modify:
- Table headers and column processing
- Filename parsing logic
- Configuration options

### 🤝 Want to Make It Better?
Check out [CONTRIBUTING.md](CONTRIBUTING.md) for possibilities ahead! This project is ripe for expansion, and I'd love to see it grow beyond its humble beginnings. 

## 🎮 Using MisterLister

### Getting Started
Simply drag and drop your files into the welcoming drop zone, or click the "Add Files" button to browse. Need more files later? No problem - you can add more at any time!

### Working with Your Data
The table interface gives you full control:
- Sort any column by clicking its header
- Right-click column headers to hide/show columns as needed
- Select multiple rows with Ctrl/Shift + Click
- Copy selected data to clipboard with Ctrl+C
- Delete rows with a right-click menu
- Select all entries with Ctrl+A

### Fine-Tune the Display
Use the bottom bar controls to make it perfect:
- Adjust font size with the +/- buttons
- Set comfortable row height spacing
- Preview how your list will look when printed
- Print your formatted list
- Clear all entries when you're done
- Access configuration options

### Print & Preview
Before printing, use the preview button to check formatting. When you're happy with how it looks, hit print! Border styles and colors can be customized in the config menu.

The interface is designed to be clean and intuitive - everything you need is just a click away. Start with a simple file drop and explore the features as you need them!

## ⚙️ Configuration Options

Access the configuration dialog to customize MisterLister to your needs:

### Format Settings
These settings sync with the +/- buttons and row height controls in the main interface:
- Font size: Adjust text size for comfortable viewing
- Row height: Set spacing between list entries
- Remember formatting: Save your preferred format settings between sessions

### Print Settings
- Border style: Choose between solid, dashed, or dotted borders
- Border color: Adjust border darkness with the slider
- Printer selection: Pick your preferred printer

### File Management
- Default directory: Set where file dialogs open initially
- Backup directory: Set an alternate default location (useful when primary directory is on an unreliable network drive)
- Remember last directory: Automatically open to your last used folder

### Startup Behavior
- Show 'Add Files' dialog: Choose whether to prompt for files on launch
- Remember window position: Save window size and location between sessions

All settings are saved automatically when clicking "Save" and persist between application launches.

## 📜 License

MIT License

Copyright (c) 2025 Ian Schuepbach

Permission is hereby granted, free of charge, to any person obtaining a copy
of MisterLister and associated documentation files, to deal in MisterLister
without restriction, including without limitation the rights to use, copy,
modify, merge, publish, distribute, sublicense, and/or sell copies of
MisterLister, and to permit persons to whom it is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies of MisterLister.

MisterLister is provided "AS IS", without warranty of any kind.
For more details, see the full MIT License text at:
https://opensource.org/licenses/MIT

