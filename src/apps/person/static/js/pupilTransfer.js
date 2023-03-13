const term = document.getElementById("term");
const submitBtn = document.getElementById("submitBtn");
const personName = document.getElementById("personName");
const personNames = document.getElementById('personNames');
const toChange = document.getElementById('toChange');
const selectedNameGroup = document.getElementById('selectedNameGroup');
const searchNameGroup = document.getElementById('searchNameGroup');

// onload page
document.body.addEventListener('htmx:load', (event) => {
  if (personName.innerText == /\w+/) {
    selectedNameGroup.classList.remove('d-none');
    searchNameGroup.classList.add('d-none');
    submitBtn.disabled = false;
  } else {
    searchNameGroup.classList.remove('d-none');
    selectedNameGroup.classList.add('d-none');
    term.focus();
    submitBtn.disabled = true;
  };
})

// on change name
htmx.on("#selectedNameGroup", "htmx:beforeSwap", (event) => {
  selectedNameGroup.classList.remove('d-none');
  searchNameGroup.classList.add('d-none');
  personNames.children[0].innerHTML = '';
  submitBtn.disabled = false;
});

// click on toChange link
htmx.on("#toChange", "click", (event) => {
  searchNameGroup.classList.remove('d-none');
  term.focus();
  selectedNameGroup.classList.add('d-none');
  personName.innerHTML = '';
  term.value = '';
  submitBtn.disabled = true;
});