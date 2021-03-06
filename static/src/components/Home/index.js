import React from 'react';
import FileUploadView from '../FileUploadView';

export const Home = () =>
    <section>
        <div className="container text-center">
            <div className="well">Please upload a protocol file in HTML Filtered Format.Docx or pdf formats are not accepted.
            <ul>
              <li>1.Open your original protocol in Microsoft word 2010</li>
              <li>2.Save your protocol on your disk by clicking Save as and specify the type : HTML Filtered</li>
              <li>3.Upload your HTML file in this application</li>
            </ul>
            </div>
            <FileUploadView/>
        </div>
    </section>;