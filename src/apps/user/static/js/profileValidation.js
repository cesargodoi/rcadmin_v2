//basic
// label para e-mail input
var hint_email = document.getElementById("hint_id_email");
hint_email.innerHTML = "Enter a valid e-mail: your@mail.com";

//fields
const socialName = document.getElementById("id_social_name");
const email = document.getElementById("id_email");
const phone_1 = document.getElementById("id_phone_1");
const phone_2 = document.getElementById("id_phone_2");
const sosContact = document.getElementById("id_sos_contact");
const sosPhone = document.getElementById("id_sos_phone");

// handler function
function alertField(input, message) {
  const invalidField = document.getElementById(input);

  var invalidValueField = document.createElement("p");
  invalidValueField.classList.add("invalid-feedback");
  var invalidText = document.createTextNode(message);
  invalidValueField.appendChild(invalidText);
  invalidField.parentElement.appendChild(invalidValueField);
  invalidField.classList.add("is-invalid");
  invalidField.focus();
}

// main check function
function checkForm() {
  // checking name input
  if (
    socialName.value.length < 2 ||
    socialName.value == "" ||
    socialName.value === null
  ) {
    let message = "Please write what you would like to be called.";
    alertField("id_social_name", message);
    return false;
  }
  // checking e-mail input
  if (
    email.value.indexOf("@") == -1 ||
    email.value.indexOf(".") == -1 ||
    email.value == "" ||
    email.value == null
  ) {
    let message = "Please enter a valid email address";
    alertField("id_email", message);
    return false;
  }
  if (
    phone_1.value.length < 10 ||
    phone_1.value == "" ||
    phone_1.value === null
  ) {
    let message = "Please register a valid phone number: xx-98765.4321";
    alertField("id_phone_1", message);
    return false;
  }
  if (phone_2.value.length > 0 && phone_2.value.length < 10) {
    let message = "Please register a valid phone number: xx-98765.4321";
    alertField("id_phone_2", message);
    return false;
  }
  if (sosContact.value) {
    if (sosPhone.value.length >= 0 && sosPhone.value.length < 10) {
      let message = "Please register a valid phone number: xx-98765.4321";
      alertField("id_sos_phone", message);
      return false;
    }
  }
  if (sosPhone.value) {
    if (sosContact.value == "" || sosContact.value == null) {
      let message = "What's the name of your emergency contact?";
      alertField("id_sos_contact", message);
      return false;
    }
  }
  // submit after checked form
  document.getElementById("form").submit();
}

// **********************************
//Address filled by ZIP Code

const inputCep = document.getElementById("id_zip_code");
inputCep.addEventListener("focusout", () => {
  pesquisacep(inputCep.value);
});

function limpa_formulário_cep() {
  //Limpa valores do formulário de cep.
  document.getElementById("id_address").value = "";
  document.getElementById("id_district").value = "";
  document.getElementById("id_city").value = "";
  document.getElementById("id_state").value = "";
}

function meu_callback(conteudo) {
  if (!("erro" in conteudo)) {
    //Atualiza os campos com os valores.
    document.getElementById("id_address").value = conteudo.logradouro;
    document.getElementById("id_district").value = conteudo.bairro;
    document.getElementById("id_city").value = conteudo.localidade;
    document.getElementById("id_state").value = conteudo.uf;
  } //end if.
  else {
    //CEP não Encontrado.
    limpa_formulário_cep();
    // alert("CEP não encontrado.");
    let message = "CEP não encontrado.";
    alertField("id_zip_code", message);
  }
}

function pesquisacep(valor) {
  //Nova variável "cep" somente com dígitos.
  var cep = valor.replace(/\D/g, "");

  //Verifica se campo cep possui valor informado.
  if (cep != "") {
    //Expressão regular para validar o CEP.
    var validacep = /^[0-9]{8}$/;

    //Valida o formato do CEP.
    if (validacep.test(cep)) {
      //Preenche os campos com "..." enquanto consulta webservice.
      document.getElementById("id_address").value = "...";
      document.getElementById("id_district").value = "...";
      document.getElementById("id_city").value = "...";
      document.getElementById("id_state").value = "...";

      //Cria um elemento javascript.
      var script = document.createElement("script");

      //Sincroniza com o callback.
      script.src =
        "https://viacep.com.br/ws/" + cep + "/json/?callback=meu_callback";

      //Insere script no documento e carrega o conteúdo.
      document.body.appendChild(script);
    } //end if.
    else {
      //cep é inválido.
      limpa_formulário_cep();
      // alert("Formato de CEP inválido.");
      let message = "Formato de CEP inválido.";
      alertField("id_zip_code", message);
    }
  } //end if.
  else {
    //cep sem valor, limpa formulário.
    limpa_formulário_cep();
  }
}

// *******************************
