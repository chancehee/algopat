import { useNavigate } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBars, faXmark } from "@fortawesome/free-solid-svg-icons";
import { useEffect, useState } from "react";
import { loginUser } from "@/atoms/user.atom";
import logo from "@/assets/img/logo.png";
import style from "./Header.module.css";

export const Header = () => {
  const navigate = useNavigate();
  const [isOpen, setIsOpen] = useState(false);

  const changeOpen = () => {
    setIsOpen((prev) => !prev);
  };

  const moveNav = (url: string) => {
    setIsOpen((prev) => !prev);
    navigate(url);
  };

  useEffect(() => {
    loginUser();
  }, []);

  return (
    <div className={style.header}>
      <img className={style.logo} onClick={() => navigate("/")} src={logo} />
      <div
        className={isOpen ? style.menu : style.menu + " " + style.menu_false}
      >
        <div onClick={() => moveNav("/code")}>코드분석</div>
        <div onClick={() => moveNav("/ranking")}>랭킹</div>
        <div onClick={() => moveNav("/community")}>커뮤니티</div>
        <div
          onClick={() => {
            window.open(
              "https://github.com/login/oauth/authorize?client_id=62a8bd9fd0300fdc6d37&redirect_uri=https://algopat.kr/login-process"
            );
          }}
        >
          로그인
        </div>
      </div>
      <div className={style.bars}>
        {!isOpen ? (
          <FontAwesomeIcon icon={faBars} onClick={changeOpen} />
        ) : (
          <FontAwesomeIcon icon={faXmark} onClick={changeOpen} />
        )}
      </div>
    </div>
  );
};
