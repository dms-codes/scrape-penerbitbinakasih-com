# Librari Book Price Comparator

This Python script scrapes book data from a website, allows users to view and compare prices from different sellers, and provides the option to tweet an inquiry to a specific seller. The script is designed for Librari, a bookstore.

## Features

- Scrapes book data, including titles, authors, prices, descriptions, and more, from a website.
- Provides a graphical user interface (GUI) for users to view and compare book prices from different sellers.
- Calculates the breakeven price for each book.
- Allows users to copy the URL for easy sharing.
- Offers a tweet feature that generates a tweet with hashtags and a pre-filled inquiry to a seller.
- Supports copying book titles and descriptions to the clipboard.
- Saves book thumbnails as image files.

## Usage

1. Modify the script to set your desired configurations:
   - Set the `PHONE` variable to your phone number for WhatsApp inquiries.
   - Configure the `HOMEPAGE` URL to the target website.
   - Set the `FILENAME` for the CSV data file.
   - Customize the `COLUMNS` variable for the CSV columns.
   - Modify other settings like `HEADERS`, `UI_FILENAME`, and more, as needed.

2. Run the script by executing the following command in your terminal:

   ```bash
   python your_script_name.py
   ```

3. The GUI will appear, allowing you to enter book numbers or navigate between books. You can view prices, descriptions, and other details.

4. Use the "Copy URL" button to copy the seller's URL to the clipboard, making it easy to share.

5. Utilize the "Tweet" button to generate a tweet with pre-filled content for inquiries to sellers.

6. Click on the "Save Image" button to save the book's thumbnail as an image file.

## Example

Suppose you have configured the script and run it with the following settings:

- `PHONE = '6287899000416'`
- `HOMEPAGE = 'http://www.penerbitbinakasih.com/'`
- `FILENAME = 'data-binakasih.csv'`
- `COLUMNS` includes various book information columns.

After running the script, you will see a GUI that allows you to interact with the book data and perform the mentioned actions.

## License

This script is provided under the [MIT License](LICENSE).
```

