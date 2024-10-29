import React from 'react'
import { useNavigate } from 'react-router-dom'
import Box from '@mui/material/Box'
import IconButton from '@mui/material/IconButton'
import OutlinedInput from '@mui/material/OutlinedInput'
import InputLabel from '@mui/material/InputLabel'
import InputAdornment from '@mui/material/InputAdornment'
import FormControl from '@mui/material/FormControl'
import TextField from '@mui/material/TextField'
import Visibility from '@mui/icons-material/Visibility'
import VisibilityOff from '@mui/icons-material/VisibilityOff'
import Button from '@mui/material/Button'
import Snackbar from '@mui/material/Snackbar'
import Alert from '@mui/material/Alert'

export default function Register(props) {
  const [email, setEmail] = React.useState('')
  const [password, setPassword] = React.useState('')
  const [passwordConfirmation, setPasswordConfirmation] = React.useState('')
  const [name, setName] = React.useState('')
  const navigate = useNavigate()
  const [showPassword, setShowPassword] = React.useState(false)
  const [showPasswordConfirmation, setShowPasswordConfirmation] =
    React.useState(false)
  const [showSnackbar, setShowSnackbar] = React.useState(false)
  const [snackbarMessage, setSnackbarMessage] = React.useState('')

  const handleClickShowPassword = () => setShowPassword((show) => !show)
  const handleMouseDownPassword = (event) => {
    event.preventDefault()
  }
  const handleClickShowPasswordConfirmation = () =>
    setShowPasswordConfirmation((show) => !show)
  const handleMouseDownPasswordConfirmation = (event) => {
    event.preventDefault()
  }

  React.useEffect(() => {
    if (props.token) {
      navigate('/history')
    }
  }, [props.token, navigate])

  const handleRegister = async () => {
    try {
      const response = await fetch('http://localhost:5005/register', {
        method: 'POST',
        body: JSON.stringify({
          email,
          password,
          passwordconfirmation: passwordConfirmation,
          name,
        }),
        headers: {
          'Content-type': 'application/json',
        },
      })

      const data = await response.json()

      if (response.status === 400 || response.status === 409) {
        setSnackbarMessage(data)
        setShowSnackbar(true)
      } else if (response.status === 201 && data.access_token) {
        localStorage.setItem('token', data.access_token)
        props.setToken(data.access_token)
        navigate('/profile')
      }
    } catch (error) {
      console.error('Registration error:', error)
      setSnackbarMessage('Registration failed. Please try again.')
      setShowSnackbar(true)
    }
  }

  const handleCancel = () => {
    navigate('/landpage')
  }

  return (
    <div
      className="registerPage"
      style={{
        display: 'flex',
        height: '80vh',
        justifyContent: 'center',
        alignItems: 'center',
        overflow: 'auto',
      }}>
      <Box
        component="form"
        sx={{
          '& > :not(style)': {
            m: 1,
            width: '90%',
            maxWidth: '30rem',
          },
        }}
        noValidate
        autoComplete="off"
        style={{
          justifyContent: 'center',
          padding: '1rem',
          width: '80%',
          maxWidth: '30rem',
          display: 'flex',
          alignItems: 'center',
          flexDirection: 'column',
          backgroundColor: '#ffffff',
        }}>
        <h2>Register</h2>
        <TextField
          id="email"
          required
          label="Email"
          variant="outlined"
          onChange={(e) => setEmail(e.target.value)}
        />
        <TextField
          id="userName"
          required
          label="User Name"
          variant="outlined"
          onChange={(e) => setName(e.target.value)}
        />
        <FormControl variant="outlined" required>
          <InputLabel htmlFor="outlined-adornment-password">
            Password
          </InputLabel>
          <OutlinedInput
            id="outlined-adornment-password"
            type={showPassword ? 'text' : 'password'}
            endAdornment={
              <InputAdornment position="end">
                <IconButton
                  aria-label="toggle password visibility"
                  onClick={handleClickShowPassword}
                  onMouseDown={handleMouseDownPassword}
                  edge="end">
                  {showPassword ? <VisibilityOff /> : <Visibility />}
                </IconButton>
              </InputAdornment>
            }
            label="Password"
            required={true}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </FormControl>
        <FormControl variant="outlined" required>
          <InputLabel htmlFor="outlined-adornment-password-confirmation">
            Password Confirmation
          </InputLabel>
          <OutlinedInput
            id="outlined-adornment-password-confirmation"
            type={showPasswordConfirmation ? 'text' : 'password'}
            endAdornment={
              <InputAdornment position="end">
                <IconButton
                  aria-label="toggle password visibility"
                  onClick={handleClickShowPasswordConfirmation}
                  onMouseDown={handleMouseDownPasswordConfirmation}
                  edge="end">
                  {showPasswordConfirmation ? (
                    <VisibilityOff />
                  ) : (
                    <Visibility />
                  )}
                </IconButton>
              </InputAdornment>
            }
            label="Password Confirmation"
            required={true}
            value={passwordConfirmation}
            onChange={(e) => setPasswordConfirmation(e.target.value)}
          />
        </FormControl>
        {password !== passwordConfirmation && (
          <p style={{ color: 'red' }}>
            The Password does not match! Please double check!
          </p>
        )}
        <Button
          variant="outlined"
          onClick={handleRegister}
          id="submitButton"
          disabled={!(password === passwordConfirmation)}>
          Submit
        </Button>
        <Button variant="outlined" onClick={handleCancel} id="cancelButton">
          Cancel
        </Button>
      </Box>

      <Snackbar
        open={showSnackbar}
        autoHideDuration={6000}
        onClose={() => setShowSnackbar(false)}>
        <Alert
          onClose={() => setShowSnackbar(false)}
          severity="error"
          sx={{ width: '100%' }}>
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </div>
  )
}
