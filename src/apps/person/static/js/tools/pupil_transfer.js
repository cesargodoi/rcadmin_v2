const searchForm = document.getElementById("searchForm");
const personName = document.getElementById("personName");
const personNames = document.getElementById('personNames');
const toChange = document.getElementById('toChange');

// onload page
document.body.addEventListener('htmx:load', (event) => {
  if (personName.innerText) {
    searchForm.classList.add('d-none');
    toChange.classList.remove('d-none');
  } else {
    searchForm.classList.remove('d-none');
    toChange.classList.add('d-none');
  };
})

// on change name
htmx.on("#personName", "htmx:beforeSwap", (event) => {
  searchForm.classList.add('d-none');
  toChange.classList.remove('d-none');
});

// click on toChange link
htmx.on("#toChange", "click", (event) => {
  searchForm.classList.remove('d-none');
  toChange.classList.add('d-none');
  personName.innerText = '';
  searchForm.children[0].children[0].value = '';
  if (personNames.children[0]) {
    personNames.children[0].innerHTML = '';
  }
});