function FirmType() {
    if (document.getElementById('id_firm_0').checked) {
        document.getElementById('company_radio').style.display = 'flex';
        document.getElementById("id_company_0").required = true;
        document.getElementById("id_company_1").required = true;
        document.getElementById("id_company_name").required = false;
        console.log("hey thr");
    }

    if (document.getElementById('id_firm_1').checked) {

        document.getElementById('company_radio').style.display = 'none';
        document.getElementById("id_company_0").required = false;
        document.getElementById("id_company_1").required = false;
        document.getElementById("id_company_name").required = false;
        console.log("hello i m here")
    }
        console.log("hello i m here from outer")
    document.getElementById('company_name').style.display = 'none';


}
function CompanyCheck() {


    if (document.getElementById('id_company_0').checked) {
        document.getElementById('company_name_label').style.display = 'inline-block';
        document.getElementById('company_name_label').innerHTML="Company Name :";
        document.getElementById('company_name').style.display = 'inline-block';
         console.log("new company checked")
        document.getElementsByTagName("id_company_name").setAttribute('required', true);
        document.getElementById("id_company_name").required = true;

    }
    else if (document.getElementById('id_company_1').checked) {
        console.log("hey 2")
        document.getElementById('company_name_label').style.display = 'inline-block';
        document.getElementById('company_name_label').innerHTML="Company Code :";

        document.getElementById('company_name').style.display = 'inline-block';

        document.getElementById("id_company_name").required = true;
    }
    else {
        console.log("hey 3")
        document.getElementById('company_name').style.display = 'none';
    }
}
