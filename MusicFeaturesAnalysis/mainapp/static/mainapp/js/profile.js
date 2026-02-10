document.addEventListener("DOMContentLoaded", function () {
	document.getElementById("predictBtn").addEventListener("click", function() {
		fetch("/load_analizer_info/", {
			method: "GET",
			headers: {
				"X-Requested-With": "XMLHttpRequest"
			}
		})
		.then(res => res.json())
		.then(data => {
			document.getElementById("predictModalBody").textContent =
                data.status === 200 ? data.data : data.error;
			var modal = new bootstrap.Modal(document.getElementById('predictModal'));
			modal.show();
		})
		.catch(err => {
			document.getElementById("predictModalBody").textContent = "Error fetching data!";
			var modal = new bootstrap.Modal(document.getElementById('predictModal'));
			modal.show();
		});
	});

    document.getElementById("statBtn").addEventListener("click", function() {
        fetch("/profile/stats/", {
            method: "GET",
            headers: { "X-Requested-With": "XMLHttpRequest" }
        })
        .then(res => res.json())
        .then(res => {
            if (res.status === 200) {
                const stats = res.data;
    
                let tableHTML = `<div class="table"><table class="table table-sm table-borderless mb-0">`;
    
                for (const [key, value] of Object.entries(stats)) {
                    tableHTML += `
                        <tr>
                            <td class="fw-bold text-center pe-3">${key}:</td>
                            <td>${value}</td>
                        </tr>
                    `;
                }
    
                tableHTML += `</table></div>`;
    
                document.getElementById("statsModalBody").innerHTML = tableHTML;
                new bootstrap.Modal(document.getElementById('statsModal')).show();
            }
        })
        .catch(err => {
            document.getElementById("statsModalBody").textContent = "Error fetching data!";
            new bootstrap.Modal(document.getElementById('statsModal')).show();
        });
    });
});

