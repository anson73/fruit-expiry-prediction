import React from 'react'
import { useNavigate } from 'react-router-dom'
import Avatar from '@mui/material/Avatar'
import Box from '@mui/material/Box'
import TextField from '@mui/material/TextField'
import IconButton from '@mui/material/IconButton'
import OutlinedInput from '@mui/material/OutlinedInput'
import InputLabel from '@mui/material/InputLabel'
import InputAdornment from '@mui/material/InputAdornment'
import FormControl from '@mui/material/FormControl'
import Visibility from '@mui/icons-material/Visibility'
import VisibilityOff from '@mui/icons-material/VisibilityOff'
import Button from '@mui/material/Button'
import CloudUploadIcon from '@mui/icons-material/CloudUpload'
import Snackbar from '@mui/material/Snackbar'
import Alert from '@mui/material/Alert'

const Profile = () => {
  const [email, setEmail] = React.useState('')
  const [daysNotify, setDaysNotify] = React.useState(3)
  const [password, setPassword] = React.useState('')
  const [newPassword, setNewPassword] = React.useState('')
  const [newPasswordConfirmed, setNewPasswordConfirmed] = React.useState('')
  const [showPassword, setShowPassword] = React.useState(false)
  const [showSnackbar, setShowSnackbar] = React.useState(false)
  const [snackbarMessage, setSnackbarMessage] = React.useState('')
  const navigate = useNavigate()
  const [image, setImage] = React.useState(null)

  React.useEffect(() => {
    const fetchProfile = async () => {
      try {
        const token = localStorage.getItem('token')
        const response = await fetch('http://localhost:5005/profile', {
          method: 'GET',
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        })
        if (response.ok) {
          const data = await response.json()
          setEmail(data.email)
          setDaysNotify(data.default_days)
        } else {
          console.error('Failed to fetch profile data')
        }
      } catch (error) {
        console.error('Error fetching profile:', error)
      }
    }

    fetchProfile()
  }, [])

  const handleClickShowPassword = () => setShowPassword((show) => !show)
  const handleMouseDownPassword = (event) => {
    event.preventDefault()
  }

  const handleImageUpdate = (event) => {
    const file = event.target.files[0]
    if (file) {
      const url = URL.createObjectURL(file)
      setImage(url)
      console.log(url)
    }
  }

  const handleSubmit = async () => {
    try {
      const token = localStorage.getItem('token')
      console.log(token)
      const response = await fetch('http://localhost:5005/profile', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          password: password,
          newpassword: newPassword,
          newpasswordconfirmation: newPasswordConfirmed,
          defaultdays: daysNotify,
        }),
      })

      if (response.ok) {
        const data = await response.json()
        console.log('Profile updated:', data)
        navigate('/history')
      } else {
        const errorData = await response.text()
        setSnackbarMessage(errorData)
        setShowSnackbar(true)
      }
    } catch (error) {
      console.error('Error updating profile:', error)
    }
  }

  const handleCancel = () => {
    navigate('/history')
  }

  return (
    <div
      style={{
        padding: '10rem 0rem',
        display: 'flex',
        alignItems: 'center',
        flexDirection: 'column',
        backgroundColor: '#ffffff',
      }}>
      <Box
        component="form"
        sx={{
          '& > :not(style)': {
            m: 1,
            width: '90%',
          },
        }}
        noValidate
        autoComplete="off"
        style={{
          width: '80%',
          maxWidth: '30rem',
          display: 'flex',
          alignItems: 'center',
          flexDirection: 'column',
          backgroundColor: '#ffffff',
        }}>
        <Avatar
          alt="Profile Image"
          src={image}
          style={{ width: '15rem', height: '15rem' }}
        />
        <Button
          variant="contained"
          component="label"
          fullWidth
          startIcon={<CloudUploadIcon />}
          sx={{ marginTop: 1 }}>
          Upload Avatar
          <input type="file" hidden onChange={handleImageUpdate} />
        </Button>

        <TextField
          id="email"
          required
          label="Email"
          variant="outlined"
          value={email || ''}
          onChange={(e) => setEmail(e.target.value)}
        />

        <FormControl variant="outlined" required>
          <InputLabel>Password</InputLabel>
          <OutlinedInput
            type={showPassword ? 'text' : 'password'}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
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
          />
        </FormControl>

        <FormControl variant="outlined" required>
          <InputLabel>New Password</InputLabel>
          <OutlinedInput
            type={showPassword ? 'text' : 'password'}
            value={newPassword || ''}
            onChange={(e) => setNewPassword(e.target.value)}
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
          />
        </FormControl>

        <FormControl variant="outlined" required>
          <InputLabel>New Password Confirmation</InputLabel>
          <OutlinedInput
            type={showPassword ? 'text' : 'password'}
            value={newPasswordConfirmed || ''}
            onChange={(e) => setNewPasswordConfirmed(e.target.value)}
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
          />
        </FormControl>

        <TextField
          id="notificationTime"
          required
          label="Notify Days before Expiry"
          variant="outlined"
          type="number"
          value={daysNotify || ''}
          onChange={(e) => setDaysNotify(e.target.value)}
        />

        <Button variant="outlined" onClick={handleSubmit}>
          Submit
        </Button>
        <Button variant="outlined" onClick={handleCancel}>
          Cancel
        </Button>
      </Box>

      <Snackbar
        open={showSnackbar}
        autoHideDuration={6000}
        onClose={() => setShowSnackbar(false)}>
        <Alert onClose={() => setShowSnackbar(false)} severity="error">
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </div>
  )
}

export default Profile
