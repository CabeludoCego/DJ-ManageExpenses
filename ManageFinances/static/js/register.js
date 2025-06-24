console.log("register working");

const usernameField = document.querySelector("#usernameField");
const userFeedBackArea = document.querySelector(".user-invalid-feedback");
const usernameSuccess = document.querySelector(".usernameSuccessOutput");

usernameField.addEventListener("keyup", (e) => {

	const usernameVal = e.target.value;
	usernameSuccess.style.display = "block";
	usernameSuccess.textContent = 'Checking for availability...';

	usernameField.classList.remove("is-invalid");
	userFeedBackArea.style.display="none";
	
	if(usernameVal.length > 0) {
		fetch('/auth/validate-username',{
			body: JSON.stringify({
				'username': usernameVal,
			}), 
			method: "POST",
		})
		.then(res => res.json())
		.then(data => {
			usernameSuccess.style.display = "none";
			if(data.username_error){
				usernameField.classList.add("is-invalid"); // Bootstrap class
				userFeedBackArea.style.display="block";
				userFeedBackArea.innerHTML = `
					<p>${data.username_error}</p>
				`;
				submitBtn.disabled = True;
			} else {
				submitBtn.removeAttribute("disabled");
			}
		})
	}
})


const emailField = document.querySelector("#emailField");
const emailFeedBackArea = document.querySelector(".email-invalid-feedback");

emailField.addEventListener("keyup", (e) => {
	const emailVal = e.target.value;
	console.log('email being typed:', emailVal);

	emailField.classList.remove("is-invalid");
	emailFeedBackArea.style.display="none";
	
	if(emailVal.length > 0) {
		fetch('/auth/validate-email',{
			body: JSON.stringify({
				'email': emailVal,
			}), 
			method: "POST",
		})
		.then(res => res.json())
		.then(data => {
			console.log('data', data);
			if(data.email_error){
				emailField.classList.add("is-invalid"); // Bootstrap class
				emailFeedBackArea.style.display="block";
				emailFeedBackArea.innerHTML = `
					<p>${data.email_error}</p>
				`;
				submitBtn.disabled = True;
			} else {
				submitBtn.removeAttribute("disabled");
			}
		})
	}

})

const passwordField = document.querySelector("#passwordField");
const showPasswordToggle = document.querySelector(".showPasswordToggle");
const handleToggleInput = (e) => {
	if(showPasswordToggle.textContent == 'SHOW'){
		showPasswordToggle.textContent = 'HIDE';
		passwordField.setAttribute("type", "text");
	} else {
		showPasswordToggle.textContent = 'SHOW';
		passwordField.setAttribute("type", "password");
	}

};

showPasswordToggle.addEventListener("click", handleToggleInput)

const submitBtn = document.querySelector(".submit-btn");

function registerFormFeedback(field, fieldName, error_type) {

	fieldName.addEventListener("keyup", (e) => {
		const fieldValue = e.target.value;

		fieldName.classList.remove("is-invalid");
		feedBackArea.style.display="none";
			
		if(fieldValue.length > 0) {
			fetch("/auth/validate-${field}",{
				body: JSON.stringify({
					"${field}": fieldValue,
				}), 
				method: "POST",
			})
			.then(res => res.json())
			.then(data => {
				console.log('data', data);
				if(data.error_type){
					fieldName.classList.add("is-invalid"); // Bootstrap class
					feedBackArea.style.display="block";
					feedBackArea.innerHTML = `
						<p>${data.error_type}</p>
					`;
				}
			})
		}
	})
}