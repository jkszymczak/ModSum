{

  description = "Python dev Env 4 PIP";
  nixConfig.bash-prompt = "[ Python ]-> ";
  inputs = { nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable"; };

  outputs = { self, nixpkgs }:
    let
    pkgs = nixpkgs.legacyPackages.x86_64-linux.pkgs;
    libs = ps: with ps; 
      [
        pycodestyle
        django
	      django-crispy-bootstrap4
        django-crispy-forms
      ];
    in
      {
        devShells.x86_64-linux.default = pkgs.mkShell {
          name = "Python";
          buildInputs = with pkgs; [
            (python311.withPackages libs)
            jmeter
          ];
        };

      };
}
