<template>
  <div>
    Account Index Page
  </div>
</template>

<script>
export default {
  name: "AccountPage",
  data() {
    return {
      form: {
        currentPassword: "",
        newPassword: "",
        confirmPassword: "",
      },
    };
  },
  methods: {
    updatePassword() {
      // Simple form validation
      if (this.form.newPassword !== this.form.confirmPassword) {
        alert("New passwords do not match!");
        return;
      }
      alert("Password updated successfully!");
    },
    resetPassword() {
      alert("A password reset link has been sent to your email.");
    },
  },
};
</script>
