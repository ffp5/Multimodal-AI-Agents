"use client";
import React, { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { MenuIcon, XIcon } from "lucide-react";

enum ActiveTab {
	HOME = 0,
	INVEST = 1,
	ABOUT = 2,
}

const NavBar = () => {
	const [activeTab, setActiveTab] = useState<ActiveTab>(ActiveTab.HOME);
	const [isMenuOpen, setIsMenuOpen] = useState<boolean>(false);

	const pathname = usePathname();
	const router = useRouter();

	useEffect(() => {
		if (pathname === "/") {
			setActiveTab(0);
		} else if (pathname.includes("/invest")) {
			setActiveTab(1);
		} else if (pathname.includes("/about")) {
			setActiveTab(2);
		}
	}, [pathname]);

	return (
		<div className="relative z-49">
			<div className="flex items-center justify-between px-8 h-[72px] sm:px-4 border-b border-b-black bg-white">
				<div className="flex items-center gap-16 h-full">
					<div
						className="cursor-pointer text-xl font-bold"
						onKeyDown={() => router.push("/")}
						onClick={() => router.push("/")}
					>
						Trip Planner
					</div>
					<div className="hidden sm:flex items-center gap-4 h-full">
						<Link
							href="/about"
							className={`px-4 h-full leading-[72px] font-bold ${
								activeTab === ActiveTab.ABOUT
									? "border-b-4 border-b-black"
									: "text-black"
							}`}
						>
							About
						</Link>
					</div>
				</div>
				<button
					className="sm:hidden block"
					type="button"
					onClick={() => setIsMenuOpen(!isMenuOpen)}
				>
					{isMenuOpen ? <XIcon /> : <MenuIcon />}
				</button>
			</div>
			{isMenuOpen && (
				<div className="sm:hidden py-4">
					<Link
						href="/about"
						className={`block px-8 py-2 ${
							activeTab === ActiveTab.ABOUT
								? "bg-securdWhite text-securdBlack"
								: "text-securdWhite"
						}`}
					>
						About
					</Link>
				</div>
			)}
		</div>
	);
};

export default NavBar;
