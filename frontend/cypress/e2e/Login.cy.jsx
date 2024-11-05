// register
// 1. password  -> len, complexity,
// 2. email -> format
describe('<Login />', () => {
  beforeEach(() => {
    cy.visit('http://localhost:3000')

    cy.get('#Login').click()
    cy.url().should('include', '/login')
  })
  it('renders all fields', () => {
    // cy.visit('http://localhost:3000/login')
    cy.get('#email').should('be.visible')
    cy.get('#outlined-adornment-password').should('be.visible')
    cy.get('#login').should('be.visible')
    cy.get('#cancelButton').should('be.visible')
  })

  it('wrong email', () => {
    // cy.visit('http://localhost:3000/login')
    cy.get('#email').type('wrong@email.com')
    cy.get('#outlined-adornment-password').type('wrongPassword')

    cy.get('#login').click()

    cy.contains('email not exist or password not correct').should('be.visible')
  })

  it('wrong password', () => {
    // cy.visit('http://localhost:3000/login')
    cy.get('#email').type('z56@email.com')
    cy.get('#outlined-adornment-password').type('wrongPassword')

    cy.get('#login').click()

    cy.contains('email not exist or password not correct').should('be.visible')
  })

  it('successful logins', () => {
    cy.visit('http://localhost:3000/register')
    cy.get('#email').type('zqq2@gmail.com')
    cy.get('#userName').type('Oswald')
    cy.get('#outlined-adornment-password').type('8888')
    cy.get('#outlined-adornment-password-confirmation').type('8888')
    cy.contains('The Password does not match! Please double check!').should(
        'not.exist'
    )
    cy.get('#submitButton').click()
    cy.url().should('include', '/profile')
    cy.get('#Logout').click()

    cy.visit('http://localhost:3000/login')
    cy.get('#email').type('zqq2@gmail.com')
    cy.get('#outlined-adornment-password').type('8888')

    cy.intercept('POST', '/login').as('loginRequest')
    cy.get('#login').click()
    cy.wait('@loginRequest')
    cy.window().then((content) => {
      const token = content.localStorage.getItem('token')
      expect(token).to.exist
    })
    cy.url().should('include', '/history')
    
  })

  it('successful cancel login', () => {
    cy.get('#cancelButton').click()
    cy.url().should('include', '/landpage')
  })
})
