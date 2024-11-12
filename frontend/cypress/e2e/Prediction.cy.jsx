// register -> Prediction
import dayjs from "dayjs";

describe("<prediction testing />", () => {
  it("renders all fields", () => {
    cy.visit("http://localhost:3000/register");
    cy.get("#email").type("7021@gmail.com");
    cy.get("#userName").type("Oswald");
    cy.get("#outlined-adornment-password").type("8888");
    cy.get("#outlined-adornment-password-confirmation").type("8888");
    cy.contains("The Password does not match! Please double check!").should(
      "not.exist"
    );
    cy.get("#submitButton").click();
    cy.url().should("include", "/profile");
    cy.get("#CancelBotton").click();
    cy.get("#Prediction").click();

    cy.url().should("include", "/prediction");
    cy.get("#imageUpload").should("exist");
    cy.get("#fruitType").should("be.visible");
    cy.get("#refridgerationForm").should("be.visible");
    cy.contains("label", "Purchase Date")
      .next()
      .find('button[aria-label="Choose date"]')
      .as("calendarButton")
      .should("be.visible");
    cy.get("#predictButton").should("be.visible");
  });

  // it("Test future dates", () => {
  //   cy.visit("http://localhost:3000/register");
  //   cy.get("#email").type("12111@gmail.com");
  //   cy.get("#userName").type("Oswald");
  //   cy.get("#outlined-adornment-password").type("8888");
  //   cy.get("#outlined-adornment-password-confirmation").type("8888");
  //   cy.contains("The Password does not match! Please double check!").should(
  //     "not.exist"
  //   );
  //   cy.get("#submitButton").click();
  //   cy.get("#CancelBotton").click();
  //   cy.get("#Prediction").click();

  //   cy.contains("label", "Purchase Date")
  //     .next()
  //     .find('button[aria-label="Choose date"]')
  //     .as("calendarButton")
  //     .click();
  //   cy.contains("Next").click();
  //   cy.contains("24").click();
  // });

  it("Standard operation flow", () => {
    cy.visit("http://localhost:3000/register");
    cy.get("#email").type("812@gmail.com");
    cy.get("#userName").type("Oswald");
    cy.get("#outlined-adornment-password").type("8888");
    cy.get("#outlined-adornment-password-confirmation").type("8888");
    cy.contains("The Password does not match! Please double check!").should(
      "not.exist"
    );
    cy.get("#submitButton").click();
    cy.url().should("include", "/profile");
    cy.get("#CancelBotton").click();
    cy.get("#Prediction").click();

    cy.url().should("include", "/prediction");
    cy.get("#imageUpload").should("exist");
    cy.get("#fruitType").should("be.visible");
    cy.get("#refridgerationForm").should("be.visible");
    cy.contains("label", "Purchase Date")
      .next()
      .find('button[aria-label="Choose date"]')
      .as("calendarButton")
      .should("be.visible");
    cy.get("#predictButton").should("be.visible");
  });

  it("test dateSelect", () => {
    cy.visit("http://localhost:3000/register");
    cy.get("#email").type("833752921@gmail.com");
    cy.get("#userName").type("Oswald");
    cy.get("#outlined-adornment-password").type("8888");
    cy.get("#outlined-adornment-password-confirmation").type("8888");
    cy.contains("The Password does not match! Please double check!").should(
      "not.exist"
    );
    cy.get("#submitButton").click();
    cy.url().should("include", "/profile");
    cy.get("#CancelBotton").click();
    cy.get("#Prediction").click();

    cy.url().should("include", "/prediction");

    cy.get('#fruitType').type('apple');
    cy.get('#demo-simple-select-label').click();
    // cy.get('#select_false').click();
    // cy.contains('li', 'True').click()
  
    const element =  cy.contains('label', 'Purchase Date').parent().find('input')
    element.clear().type('12/10/2026')
    cy.wait(500)
    cy.get('#predictButton').should('be.disabled');
    cy.contains('Please Input a valid consumption date that is in the future!')
  
    element.focus().clear()
    element.type('12/10/2023')
    cy.wait(500)
    cy.get('#predictButton').should('not.be.disabled');
    cy.get('#predictButton').click();
    cy.get('#prediction-result').should('contain.text', 'Estimated Expiry');
  });
});
