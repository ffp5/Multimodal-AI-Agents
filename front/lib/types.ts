import type { JSX } from "react";

export type LoginProduct = {
	icon: string;
	name: string;
};

export type LoginType = {
	title: string;
	description: string;
	details: string;
	id: string;
	instructions: string;
	component: JSX.Element;
	code: string;
	products?: LoginProduct[];
	entryButton?: {
		text: string;
		disabled?: boolean;
		onClick?: () => void;
	};
	preventClickthrough?: boolean;
};
