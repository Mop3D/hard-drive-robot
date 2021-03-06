import * as React from 'react';

export default class Header extends React.Component<{}, {}> {
    public render() {
       return  <header className="header">
       <ul className="header__list header__list--float-left">
         <li className="header__item"><a className="header__link" href="/robodesk">Robo-Desk</a></li>
         <li className="header__item"><a className="header__link" href="/elevator">Elevator</a></li>
         <li className="header__item"><a className="header__link" href="/files">Files</a></li>
       </ul>
       <ul className="header__list header__list--float-right">
         <li className="header__item">Info V0.2020.01.19.1</li>
       </ul>
     </header>;
    }
}
