document.addEventListener("DOMContentLoaded", function () {
    const dropZone = document.getElementById("dropZone");
    const fileInput = document.getElementById("fileInput");
    const fileInfo = document.getElementById("fileInfo");
    const uploadBtn = document.getElementById("uploadBtn");
    const loading = document.getElementById("loading");
    const responseContainer = document.getElementById("responseContainer");
    const dynamicSubHeader = document.getElementById("dynamicSubHeader");
    const errorContainer = document.getElementById("errorContainer");
    const dynamicTableBody = document.getElementById("dynamicTableBody");

    let selectedFile = null;

    // Handle click to open file dialog
    dropZone.addEventListener("click", () => fileInput.click());

    // Handle file selection
    fileInput.addEventListener("change", (event) => {
        selectedFile = event.target.files[0];
        updateFileInfo();
    });

    // Handle drag over effect
    dropZone.addEventListener("dragover", (event) => {
        event.preventDefault();
        dropZone.classList.add("dragover");
    });

    // Handle drag leave
    dropZone.addEventListener("dragleave", () => {
        dropZone.classList.remove("dragover");
    });

    // Handle drop event
    dropZone.addEventListener("drop", (event) => {
        event.preventDefault();
        dropZone.classList.remove("dragover");

        if (event.dataTransfer.files.length > 0) {
            selectedFile = event.dataTransfer.files[0];
            updateFileInfo();
        }
    });

    // Update file info text and enable upload button
    function updateFileInfo() {
        if (selectedFile) {
            fileInfo.textContent = `Selected File: ${selectedFile.name}`;
            uploadBtn.disabled = false;
        } else {
            fileInfo.textContent = "";
            uploadBtn.disabled = true;
        }
    }

    // Handle file upload
    uploadBtn.addEventListener("click", () => {
        if (!selectedFile) return;

        const formData = new FormData();
        formData.append("file", selectedFile);

        // Show loading spinner
        loading.style.display = "block";
        responseContainer.style.display = "none";
        errorContainer.style.display = "none";
        dynamicSubHeader.style.display = "none";

        // Send AJAX request using Fetch API
        fetch("/upload", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            loading.style.display = "none"; // Hide loader
            responseContainer.style.display = "block";
            
            // Mock Response (Replace this with `data` in real API)
            // data = {
            //     "Request Type": "Payment Issues",
            //     "Sub Request Type": "Payment Allocation Error",
            //     "Reason": "Incorrect fee charge on loan account",
            //     "Confidence Level": "90%",
            //     "Priority": "High",
            //     "Extracted Fields": {
            //         "Personal Information": {
            //             "Name": "John Smith",
            //             "Email": "john@example.com",
            //             "Account Number": "1234",
            //             "Loan Amount": "20000 USD",
            //             "Interest Rate": "5%",
            //             "Account Holder Name": "John Doe"
            //         }
            //     },
            //     "Duplicate Detection": "No, the issue is not resolved",
            //     "Explanation": "The customer is disputing an incorrect fee charge on their loan account and is requesting it to be removed.",
            //     "Notes": "The customer has attached a screenshot as proof that no such fee should be detected."
            // };

            // Set dynamic sub-header
            dynamicSubHeader.textContent = "Analysis";
            dynamicSubHeader.style.display = "block";

            // Clear previous table content
            dynamicTableBody.innerHTML = "";

            // Populate table with response data
            Object.entries(data).forEach(([key, value]) => {
                let formattedKey = key.replace(/_/g, " ").replace(/\b\w/g, char => char.toUpperCase()); // Format key names

                if (typeof value === "object" && value !== null) {
                    let formattedValue = "";
                    Object.entries(value).forEach(([subKey, subValue]) => {
                        if (typeof subValue === "object" && subValue !== null) {
                            formattedValue += `<strong>${subKey}:</strong><br>`;
                            Object.entries(subValue).forEach(([nestedKey, nestedValue]) => {
                                formattedValue += `&emsp; <strong>${nestedKey}:</strong> ${nestedValue}<br>`;
                            });
                        } else {
                            formattedValue += `<strong>${subKey}:</strong> ${subValue}<br>`;
                        }
                    });
                    value = `<div>${formattedValue}</div>`;
                }

                // Append row to table
                dynamicTableBody.innerHTML += `
                    <tr>
                        <th>${formattedKey}</th>
                        <td>${value || "N/A"}</td>
                    </tr>
                `;
            });
        })
        .catch(error => {
            loading.style.display = "none";
            errorContainer.textContent = "Error: " + error.message;
            errorContainer.style.display = "block";
        });
    });
});
