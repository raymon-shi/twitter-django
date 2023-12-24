const editProfileButton = document.querySelector('.edit-profile-button')
const editProfileModal = document.querySelector('.profile-modal')

editProfileButton.addEventListener('click', () => {
  editProfileModal.classList.add('is-active')
})