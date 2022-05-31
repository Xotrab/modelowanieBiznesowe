import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-starting-page',
  templateUrl: './starting-page.component.html',
  styleUrls: ['./starting-page.component.scss']
})
export class StartingPageComponent implements OnInit {

  constructor(private router: Router) { }

  ngOnInit(): void {
  }

  public nextStep() {
    this.router.navigate(["uploadFile"]);
  }
}
