import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'GuardForge AI - Analyzer';
  prompt = '';
  result: any = null;
  history: any[] = [];
  apiUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) {
    this.loadHistory();
  }

  analyzePrompt() {
    if (!this.prompt.trim()) return;
    
    this.http.post(`${this.apiUrl}/analyze`, { prompt: this.prompt }).subscribe({
      next: (res) => {
        this.result = res;
        this.loadHistory();
      },
      error: (err) => {
        console.error('Error analyzing prompt', err);
      }
    });
  }

  loadHistory() {
    this.http.get<any[]>(`${this.apiUrl}/history`).subscribe({
      next: (res) => {
        this.history = res;
      },
      error: (err) => {
        console.error('Error loading history', err);
      }
    });
  }
}
