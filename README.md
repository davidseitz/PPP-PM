# PPP-PM
Passwort-Manager
Overview

This Password Manager is a command-line based tool designed to securely store, manage, and access passwords for various websites and services. The application supports multiple users, each with their own encrypted password database. The intuitive text-based interface makes it easy to navigate through different options and manage passwords efficiently.

Features

    Multi-User Support: Multiple users can create accounts and log in with their own secure, encrypted passwords.
    Password Management:

        Add: Save new passwords along with relevant details like website URL and notes.
        Search: Quickly find passwords using a site URL or a keyword pattern.
        View: Display stored passwords for a specific site or list all entries.
        Edit: Modify existing passwords and associated details.
        Delete: Remove passwords that are no longer needed.

    Password Generation: Automatically generate strong, random passwords based on user-specified criteria (length, inclusion of uppercase letters, numbers, special characters).
    Export and Import: Export password entries to a file for backup, or import from an external file.
    Security:

        Encryption: Passwords are encrypted and stored securely.
        Password Strength Evaluation: Passwords are checked against common security standards, including length and complexity requirements.
        Pwned Password Check: Verify whether a password has been compromised in known data breaches.
        Two-Factor Authentication: Supports an additional layer of security using second-factor authentication.

Navigating the Interface:

      Use the arrow keys to navigate between options.
      Press Enter to select an option.
      Follow the on-screen instructions to add, edit, search, or delete password entries.

Main Functions

    printMenu: Displays a menu of options to the user.
    getInput: Prompts the user for input, ensuring secure and accurate data entry.
    validateUser: Checks user credentials to allow access to the password manager.
    addSitePassword: Adds a new password entry for a specified site or service.
    generatePassword: Generates a random, strong password based on user-defined criteria.
    editPassword: Modifies details of an existing password entry.
    deletePassword: Removes a password entry from the database.
    findPassword: Searches for and displays a password entry using URL or keyword pattern.
    viewAllSites: Lists all stored password entries.
    exportToFile: Exports password entries to a file for backup.

Security Notes

    All passwords are encrypted before being stored on disk.
    Use a strong, unique master password for each user account.
    Regularly back up your password entries using the export feature.
    Avoid using common or easily guessable passwords.

Contact

    For any questions, issues, or suggestions, please contact seitz.david-it23@dhbw-ravensburg.de
    