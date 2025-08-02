<script setup>
import { ref, onMounted } from 'vue'

// --- State Management ---
const notes = ref([])
const noteForm = ref({ id: null, title: '', content: '' })

const API_URL = 'http://localhost:8080' // Đảm bảo port này khớp với backend của bạn

// --- API Functions ---
async function getNotes() {
  try {
    const response = await fetch(`${API_URL}/notes/`)
    notes.value = await response.json()
  } catch (error) {
    console.error('Lỗi khi tải ghi chú:', error)
  }
}

async function handleFormSubmit() {
  const isUpdating = noteForm.value.id !== null;
  const url = isUpdating ? `${API_URL}/notes/${noteForm.value.id}` : `${API_URL}/notes/`;
  const method = isUpdating ? 'PUT' : 'POST';

  try {
    await fetch(url, {
      method: method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: noteForm.value.title, content: noteForm.value.content }),
    });
    resetForm();
    await getNotes();
  } catch (error) {
    console.error('Lỗi khi gửi form:', error);
  }
}

async function deleteNote(id) {
  if (confirm('Bạn có chắc chắn muốn xóa ghi chú này?')) {
    try {
      await fetch(`${API_URL}/notes/${id}`, { method: 'DELETE' });
      await getNotes();
    } catch (error) {
      console.error('Lỗi khi xóa ghi chú:', error);
    }
  }
}

// --- Helper Functions ---
function editNote(note) {
  noteForm.value = { ...note };
}

function resetForm() {
  noteForm.value = { id: null, title: '', content: '' };
}

// --- Lifecycle Hook ---
onMounted(() => {
  getNotes()
})
</script>

<template>
  <header>
    <h1>Ghi chú của tôi (Vue.js + FastAPI)</h1>
  </header>

  <main>
    <form @submit.prevent="handleFormSubmit" class="note-form">
      <input type="text" v-model="noteForm.title" placeholder="Tiêu đề" required>
      <textarea v-model="noteForm.content" placeholder="Nội dung" required></textarea>
      <div class="form-buttons">
        <button type="submit">{{ noteForm.id === null ? 'Thêm ghi chú' : 'Cập nhật' }}</button>
        <button type="button" v-if="noteForm.id !== null" @click="resetForm">Hủy</button>
      </div>
    </form>

    <div class="notes-list">
      <div v-for="note in notes" :key="note.id" class="note">
        <h3>{{ note.title }}</h3>
        <p>{{ note.content }}</p>
        <div class="note-actions">
          <button @click="editNote(note)">Sửa</button>
          <button @click="deleteNote(note.id)" class="delete">Xóa</button>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
  main { max-width: 600px; margin: auto; padding: 20px; }
  .note-form { background: #fff; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
  .note { background: #fff; border: 1px solid #ddd; padding: 15px; margin-bottom: 10px; border-radius: 8px; }
  .form-buttons, .note-actions { display: flex; gap: 10px; margin-top: 10px; }
  button.delete { background-color: #dc3545; }
</style>