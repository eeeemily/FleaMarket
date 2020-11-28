$(document).ready(function() {
	// First function to add new steps to the list
	$("#addSteps").click(function() {
		if ($("#newStep").val()) { // if the form is not empty 
			
			let newItem = $('#newStep').val() // get value 
			// Append the new item to the list
			$('#elements2').append("<li>" + newItem +"</li>")
			// Set the text field to empty after submit
			$('#newStep').val('')

		}
		return false;
	})

	// Second function to add new  items to the list
	$("#addItems").click(function() {
		if ($("#newItem").val()) {
			// Get the value inside the text field
			let newItem = $('#newItem').val()
			// Append the new item to the list
			$('#elements').append("<li>" + newItem +"</li>")
			// Set the text field to empty after submit
			$('#newItem').val('')

		}
		return false;
	})
	
	// create "handles" on the buttons from the HTML
	var itemBtn = $("#showEntries");
	
	var stepBtn = $("#lists");
	var clearBtn1 = $("#clear1"); 
	var clearBtn2 = $("#clear2"); 
	

	// create "handles" on the lists
	var itemList = $("#elements");
	var stepList = $("#elements2");
	

	// call the function to show the lists one by one
	display(itemBtn, itemList)
	display(stepBtn, stepList)
	hide(clearBtn1, itemList)
	hide(clearBtn2, stepList)

	




	
})

// Function to display the list one by one
function display(button, list) {
	hideItem(list)
		
	$(button).click(function() {
		// Get all childrens of the list and its length
		let children = $(list).children();
		let length = $(list).children().length;
		for (let i = 0 ; i < length; i++) {
			let currChild = (children).get(i);
			// If the current element is hidden then show it
			if (!$(currChild).is(":visible")) {
				$(currChild).show();
				break;
			}

		}
	})
}



// Function to hide the list one by one
function hide(button,list) {
	$(button).click(function() {
	
			
hideItem(list)
		
	})
}

// Function to hide all the items of the list
function hideItem(list) {
	$(list).children().hide("slow")
}
