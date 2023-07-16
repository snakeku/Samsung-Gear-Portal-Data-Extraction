// Samsung Gear Portal Data Extraction Overview: 
// This code performs data mining and ETL (Extract, Transform, Load) operations on a web page in a web browser runtime environment. 
// It extracts relevant data from the Samsung GearUp Portal web page, transforms it by cleaning and structuring the data, and loads it 
// into a CSV file for further analysis or storage. The code retrieves the total user count, sets the appropriate value in a select element, 
// calculates the "Days Since Last Login" column, and generates a CSV file containing the processed data.

// Extract the total user count
var totalCount = getTotalCount();

// Set the select element value and trigger a change event
setSelectElementValue(totalCount);

// Generate and download the CSV file after a delay of 1000 milliseconds
downloadCSVFile(1000);


function getTotalCount() {
    // This function extracts the total user count from the web page and
    // returns the number of total user count.time
    
  // Find the element by its ID
  var infoElement = document.getElementById('liveMapDataTable_info');

  // Get the text content of the element
  var infoText = infoElement.textContent;

  // Extract the count using regular expressions
  var countMatch = infoText.match(/(\d+) entries/);

  // Check if a match is found and retrieve the count
  var totalCount = countMatch ? parseInt(countMatch[1]) : 0;

  // Print the total count
  console.log('Total entries:', totalCount);

  return totalCount;
}

function setSelectElementValue(totalCount) {
    // This function sets the select element value to the previously obtained total count and triggers a change event.
    // All of the rows will be show and reflected in the table
    
  // Find the select element by its name attribute
  var selectElement = document.querySelector('select[name="liveMapDataTable_length"]');

  // Set the value of the select element to the totalCount
  selectElement.value = totalCount;

  // Dispatch a change event to trigger the update
  var event = new Event('change');
  selectElement.dispatchEvent(event);
}

function calculateDaysSinceLastLogin(inputTimeStamp){
    // This function calculates and return the days since the last user login.
    
    // Get the current date
    var currentDate = new Date();
    
    // Convert the timestamp to a Date object
    var lastLoginDate = new Date(inputTimeStamp);

    
    // Calculate the difference in days between the current date and the last login date
    var timeDifference = currentDate.getTime() - lastLoginDate.getTime();
    var daysDifference = Math.floor(timeDifference / (1000 * 3600 * 24));
    
    return daysDifference;
}

function sqlDateFormatter(inputTimeStamp){
    // This function takes in a timestamp from the server and returns a date format that is SQL date format.
    
    const dateString = inputTimeStamp;
    const date = new Date(dateString);
    const year = date.getFullYear();
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const day = date.getDate().toString().padStart(2, '0');
    const sqlDateFormat = `${year}-${month}-${day}`;
    
    return sqlDateFormat;
}

function createLocalCSV(){
    // This function looks at the data from the table, extract the data and create a CSV data.
    // The function will finally return the Blob object with CSV data
    
     // Find the table element by its ID
    var table = document.getElementById('liveMapDataTable');

    // Initialize an empty string to store the CSV data
    var csvData = '';

    csvData += 'Name' + ',' + 'Email' + ',' + 'Date' + ',' + 'Latitude' + ',' + 'Longitude' + ',' + 'LastLogin in Days' + '\n';

    // Iterate over the table rows, excluding the header row
    for (var i = 1; i < table.rows.length; i++) {
      var row = table.rows[i];

      // Extract the text content from each table cell in the row
      var name = row.cells[0].textContent;
      // formattedName is to exclude the comma in the name.
      var formattedName = '"' + name + '"';
      var email = row.cells[1].textContent;
      var timestamp = row.cells[2].textContent;
      var formattedDate = sqlDateFormatter(timestamp);
      var latLong = row.cells[3].textContent;
      var lastLogin = calculateDaysSinceLastLogin(timestamp);

      // Append the row data to the CSV string
      csvData += formattedName + ',' + email + ',' + formattedDate + ',' + latLong + ',' + lastLogin + '\n';
    }

    // Create a Blob object with the CSV data
    var blob = new Blob([csvData], { type: 'text/csv;charset=utf-8;' });
    return blob;
}

function downloadCSVFile(delay) {
    // Generates and triggers the download of a CSV file containing table data.
    // The delay is necessary as only the default 10 rows will be downloaded if delay is not set. 
    // Delay is set in the argument of the method in milliseconds before generating the CSV.
    
  setTimeout(function () {
      var blob = createLocalCSV();
      
      // Create a temporary anchor element
      var link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      
      // Set the filename for the download
      link.download = 'users_data.csv';
      
      // Programmatically click the link to trigger the download
      link.click();
      
      // Clean up the URL object
      URL.revokeObjectURL(link.href);
  }, delay);
}
