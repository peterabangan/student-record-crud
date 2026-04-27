function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createMenu('🚀 Research Tools')
      .addItem('Run Alpha Automate', 'runCronbachAnalysis')
      .addToUi();
}

function runCronbachAnalysis() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var rawSheet = ss.getSheets()[0]; 
  var dashSheet = ss.getSheetByName("Dashboard") || ss.insertSheet("Dashboard");
  
  var data = rawSheet.getDataRange().getValues();
  var headers = data[0];
  var rows = data.slice(1);
  
  // 1. STRICT LIKERT DETECTION
  var validColIndices = [];
  for (var col = 0; col < headers.length; col++) {
    // Get all numbers, ignoring blanks
    var colValues = rows.map(r => r[col]).filter(v => v !== "" && !isNaN(v) && typeof v === 'number');
    
    if (colValues.length > 0) {
      var maxVal = Math.max(...colValues);
      var minVal = Math.min(...colValues);
      
      // LIKERT CHECK: If the numbers are between 1 and 5, it's a question.
      // This will skip Grade Level (11, 12) because 11 > 5.
      // This will skip General Average (85, 90) because 90 > 5.
      if (maxVal <= 6 && minVal >= 1) {
        validColIndices.push(col);
      }
    }
  }

  var questionData = rows.map(row => validColIndices.map(index => row[index]));
  var numQuestions = validColIndices.length;
  var numResponses = questionData.length;

  if (numQuestions === 0) {
    SpreadsheetApp.getUi().alert("❌ No Likert data found. Please ensure your answers are in numerical likert form.");
    return;
  }

  dashSheet.clear();

  // 2. HEADERS & DATA TABLE
  var dynamicHeaders = ["Resp No."];
  for (var i = 1; i <= numQuestions; i++) { dynamicHeaders.push("Q" + i); }
  dynamicHeaders.push("Total");

  dashSheet.getRange(1, 1, 1, dynamicHeaders.length).setValues([dynamicHeaders]).setFontWeight("bold");
  
  var ids = [];
  for (var i = 1; i <= numResponses; i++) { ids.push([i]); }
  dashSheet.getRange(2, 1, numResponses, 1).setValues(ids);
  dashSheet.getRange(2, 2, numResponses, numQuestions).setValues(questionData);
  
  var totalColIndex = numQuestions + 2;
  dashSheet.getRange(2, totalColIndex, numResponses, 1).setFormulaR1C1("=SUM(RC[-" + numQuestions + "]:RC[-1])");

  // 3. VAR-SAMPLE ROW
  var varRowIndex = numResponses + 2;
  dashSheet.getRange(varRowIndex, 1).setValue("var-sample");
  var varRange = dashSheet.getRange(varRowIndex, 2, 1, numQuestions + 1);
  varRange.setFormulaR1C1("=VAR.S(R2C:R[-1]C)");

  // 4. SUMMARY BLOCK
  var summaryCol = totalColIndex + 2;
  var lastQLetter = getColLetter(numQuestions + 1); 
  var totalScoreLetter = getColLetter(totalColIndex);

  dashSheet.getRange(2, summaryCol).setValue("No. of items =");
  dashSheet.getRange(2, summaryCol + 1).setValue(numQuestions);
  
  dashSheet.getRange(3, summaryCol).setValue("Sum of item variances =");
  dashSheet.getRange(3, summaryCol + 1).setFormula("=SUM(B" + varRowIndex + ":" + lastQLetter + varRowIndex + ")");

  dashSheet.getRange(4, summaryCol).setValue("Variance of total scores =");
  dashSheet.getRange(4, summaryCol + 1).setFormula("=" + totalScoreLetter + varRowIndex);

  // Math references
  var sumVarCell = getColLetter(summaryCol + 1) + "3"; 
  var totalVarCell = getColLetter(summaryCol + 1) + "4"; 
  dashSheet.getRange(5, summaryCol).setValue("Cronbach's Alpha =");
  dashSheet.getRange(5, summaryCol + 1).setFormula("=(" + numQuestions + "/(" + numQuestions + "-1))*(1-(" + sumVarCell + "/" + totalVarCell + "))");

  // 5. BLUE BADGE
  var nameCell = dashSheet.getRange(6, summaryCol);
  dashSheet.getRange(6, summaryCol, 1, 3).merge();
  nameCell.setValue("Designed and Built by: Peter Paul C. Abangan")
          .setFontFamily("Impact").setFontColor("white").setBackground("#0080FF")
          .setFontWeight("bold").setFontStyle("italic").setFontSize(12).setHorizontalAlignment("left");

  dashSheet.setColumnWidths(summaryCol, 2, 180);
  SpreadsheetApp.getUi().alert("✅ Success! " + numQuestions + " questions found. Check your Dashboard for your Alpha result!");
}

function getColLetter(col) {
  var letter = "";
  while (col > 0) {
    var temp = (col - 1) % 26;
    letter = String.fromCharCode(temp + 65) + letter;
    col = (col - temp - 1) / 26;
  }
  return letter;
}