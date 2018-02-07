import React from 'react';
import FileUploadView from '../FileUploadView';
import ResultView from '../ResultView';

export const Home = () =>
    <section>
        <div className="container text-center">
            <FileUploadView/>
            <ResultView/>
        </div>
    </section>;
