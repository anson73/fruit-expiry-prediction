// register -> Prediction
describe("<prediction testing />", () => {
  it("renders all fields", () => {
    cy.visit("http://localhost:3000/register");
    cy.get("#email").type("70@gmail.com");
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

  it("Test future dates", () => {
    cy.visit("http://localhost:3000/register");
    cy.get("#email").type("121@gmail.com");
    cy.get("#userName").type("Oswald");
    cy.get("#outlined-adornment-password").type("8888");
    cy.get("#outlined-adornment-password-confirmation").type("8888");
    cy.contains("The Password does not match! Please double check!").should(
      "not.exist"
    );
    cy.get("#submitButton").click();
    cy.get("#CancelBotton").click();
    cy.get("#Prediction").click();

    cy.contains("label", "Purchase Date")
      .next()
      .find('button[aria-label="Choose date"]')
      .as("calendarButton")
      .click();
    cy.contains("Next").click();
    cy.contains("24").click();
  });

  it("Standard operation flow", () => {
    cy.visit("http://localhost:3000/register");
    cy.get("#email").type("8@gmail.com");
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
});
