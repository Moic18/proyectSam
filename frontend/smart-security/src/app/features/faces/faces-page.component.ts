import { Component } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';

import { ApiService } from '../../core/services/api.service';

interface FaceUser {
  id: number;
  name: string;
  email: string;
}

@Component({
  selector: 'app-faces-page',
  templateUrl: './faces-page.component.html',
  styleUrls: ['./faces-page.component.scss']
})
export class FacesPageComponent {
  users: FaceUser[] = [];
  uploading = false;
  message = '';

  form = this.fb.group({
    name: ['', Validators.required],
    email: ['', [Validators.required, Validators.email]],
    password: ['', Validators.required],
    files: [null]
  });

  constructor(private api: ApiService, private fb: FormBuilder) {
    this.loadUsers();
  }

  loadUsers(): void {
    this.api.get<FaceUser[]>('/faces/').subscribe(users => (this.users = users));
  }

  onFileChange(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files?.length) {
      this.form.patchValue({ files: input.files });
    }
  }

  submit(): void {
    if (this.form.invalid || !this.form.value.files) {
      this.message = 'Completa el formulario y selecciona imágenes.';
      return;
    }
    const formData = new FormData();
    formData.append('name', this.form.value.name || '');
    formData.append('email', this.form.value.email || '');
    formData.append('password', this.form.value.password || '');
    Array.from(this.form.value.files as FileList).forEach(file => formData.append('files', file));

    this.uploading = true;
    this.api.upload('/faces/enroll', formData).subscribe({
      next: response => {
        this.message = 'Usuario registrado correctamente';
        this.uploading = false;
        this.loadUsers();
      },
      error: () => {
        this.message = 'Error al registrar al usuario';
        this.uploading = false;
      }
    });
  }

  train(): void {
    this.api.post('/faces/train', {}).subscribe({
      next: () => (this.message = 'Entrenamiento iniciado'),
      error: () => (this.message = 'No hay datos suficientes para entrenar')
    });
  }
}
