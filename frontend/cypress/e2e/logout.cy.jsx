describe('<Logout />', () => {
    it('register user first and logout', () => {
      cy.visit('http://localhost:3000/register')
      cy.get('#email').type('787770013@gmail.com')
      cy.get('#userName').type('Oswald')
      cy.get('#outlined-adornment-password').type('123')
      cy.get('#outlined-adornment-password-confirmation').type('123')
      cy.contains('The Password does not match! Please double check!').should(
        'not.exist'
      )
      cy.get('#submitButton').click()
      cy.url().should('include', '/profile')
  
      cy.get('#Logout').click()
      cy.window().then((content) => {
        const token = content.localStorage.getItem('token')
        expect(token).to.be.null
      })
    })
  
    it('login user first and logout', () => {
      // cy.visit('http://localhost:3000/register')
      // cy.get('#email').type('t123')
      // cy.get('#userName').type('Oswald')
      // cy.get('#outlined-adornment-password').type('1111')
      // cy.get('#outlined-adornment-password-confirmation').type('1111')
      // cy.contains('The Password does not match! Please double check!').should(
      //   'not.exist'
      // )
      // cy.get('#submitButton').click()
      // cy.url().should('include', '/profile')
  
      // cy.get('#Logout').click()

      cy.visit('http://localhost:3000/login')
      cy.get('#email').type('t123')
      cy.get('#outlined-adornment-password').type('1111')
      cy.get('#login').click()
      cy.url().should('include', '/history')
  
      cy.get('#Logout').click()
      cy.window().then((content) => {
        const token = content.localStorage.getItem('token')
        expect(token).to.be.null
      })
    })
  })