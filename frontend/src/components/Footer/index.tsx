import imgFooterLogo from '../../assets/images/footer-logo.svg';
import "./footer.scss";

const Footer = (): JSX.Element => {
    return (
        <footer>
            <img src={imgFooterLogo} alt="AXON"/>
            ПАК Верификации 2D кодов
        </footer>
    )
}

export default Footer;